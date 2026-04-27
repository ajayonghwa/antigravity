#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import platform
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import json
from typing import Iterable, Iterator, Optional


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS chunks (
  chunk_id TEXT PRIMARY KEY,
  source TEXT NOT NULL,          -- ansys_pdf | spaceclaim_chm | pyansys_html | pyansys_text | pyansys_docstring
  title TEXT,
  locator TEXT,                  -- e.g. "p.123", "Topic/Path", "module:function"
  path TEXT NOT NULL,            -- local file path (best-effort)
  text TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  chunk_id UNINDEXED,
  source,
  title,
  locator,
  path,
  text,
  content='chunks',
  content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid, chunk_id, source, title, locator, path, text)
  VALUES (new.rowid, new.chunk_id, new.source, new.title, new.locator, new.path, new.text);
END;

CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, chunk_id, source, title, locator, path, text)
  VALUES('delete', old.rowid, old.chunk_id, old.source, old.title, old.locator, old.path, old.text);
END;

CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, chunk_id, source, title, locator, path, text)
  VALUES('delete', old.rowid, old.chunk_id, old.source, old.title, old.locator, old.path, old.text);
  INSERT INTO chunks_fts(rowid, chunk_id, source, title, locator, path, text)
  VALUES (new.rowid, new.chunk_id, new.source, new.title, new.locator, new.path, new.text);
END;
"""


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def _norm_ws(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _chunk_text(text: str, *, target_chars: int = 3500, overlap: int = 300) -> list[str]:
    text = _norm_ws(text)
    if not text:
        return []
    if len(text) <= target_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + target_chars)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [c for c in chunks if c]


class _HTMLText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self._parts.append(data)

    def text(self) -> str:
        return _norm_ws("\n".join(self._parts))


@dataclass(frozen=True)
class DocChunk:
    source: str
    title: str
    locator: str
    path: str
    text: str

    @property
    def chunk_id(self) -> str:
        # stable: source + path + locator + text hash
        return _sha1(f"{self.source}\n{self.path}\n{self.locator}\n{self.text}")


def _ensure_db(db_path: Path, *, reset: bool) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys=ON")
    if reset:
        conn.executescript(
            """
            DROP TABLE IF EXISTS chunks;
            DROP TABLE IF EXISTS chunks_fts;
            DROP TRIGGER IF EXISTS chunks_ai;
            DROP TRIGGER IF EXISTS chunks_ad;
            DROP TRIGGER IF EXISTS chunks_au;
            """
        )
    conn.executescript(SCHEMA_SQL)
    return conn


def _upsert_chunks(conn: sqlite3.Connection, chunks: Iterable[DocChunk]) -> int:
    n = 0
    cur = conn.cursor()
    for c in chunks:
        cur.execute(
            """
            INSERT INTO chunks(chunk_id, source, title, locator, path, text)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(chunk_id) DO UPDATE SET
              source=excluded.source,
              title=excluded.title,
              locator=excluded.locator,
              path=excluded.path,
              text=excluded.text
            """,
            (c.chunk_id, c.source, c.title, c.locator, c.path, c.text),
        )
        n += 1
    conn.commit()
    return n


def _iter_ansys_pdf(ansys_dir: Path) -> Iterator[DocChunk]:
    """
    Strategy:
    - Prefer pre-extracted text: <pdf>.txt (same basename) if exists.
    - Else try `pdftotext` if present.
    - Else try `pypdf` if installed.
    """
    if not ansys_dir.exists():
        return

    pdfs = sorted([p for p in ansys_dir.rglob("*.pdf") if p.is_file()])
    for pdf in pdfs:
        title = pdf.stem
        txt = pdf.with_suffix(".txt")
        if txt.exists():
            raw = txt.read_text(encoding="utf-8", errors="ignore")
            for idx, chunk in enumerate(_chunk_text(raw), start=1):
                yield DocChunk(
                    source="ansys_pdf",
                    title=title,
                    locator=f"{txt.name}#chunk{idx}",
                    path=str(txt),
                    text=chunk,
                )
            continue

        # pdftotext fallback
        pdftotext = _which("pdftotext.exe") or _which("pdftotext")
        if pdftotext:
            try:
                out_txt = pdf.with_suffix(".pdftotext.txt")
                subprocess.run(
                    [pdftotext, str(pdf), str(out_txt)],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                raw = out_txt.read_text(encoding="utf-8", errors="ignore")
                for idx, chunk in enumerate(_chunk_text(raw), start=1):
                    yield DocChunk(
                        source="ansys_pdf",
                        title=title,
                        locator=f"{pdf.name}#chunk{idx}",
                        path=str(pdf),
                        text=chunk,
                    )
                continue
            except Exception:
                pass

        # pypdf fallback
        try:
            from pypdf import PdfReader  # type: ignore

            reader = PdfReader(str(pdf))
            for page_i, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                for idx, chunk in enumerate(_chunk_text(text, target_chars=2500, overlap=200), start=1):
                    yield DocChunk(
                        source="ansys_pdf",
                        title=title,
                        locator=f"{pdf.name}#p{page_i}-chunk{idx}",
                        path=str(pdf),
                        text=chunk,
                    )
            continue
        except Exception:
            # No extraction method available; emit a small sentinel chunk so search can tell the user what to do.
            msg = (
                f"PDF text extraction unavailable for {pdf.name}. Provide {pdf.with_suffix('.txt').name} or install "
                f"`pdftotext` or `pypdf` in your venv."
            )
            yield DocChunk(source="ansys_pdf", title=title, locator=f"{pdf.name}#NO_TEXT", path=str(pdf), text=msg)


def _which(name: str) -> Optional[str]:
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for p in paths:
        cand = Path(p) / name
        if cand.exists():
            return str(cand)
    return None


def _decompile_chm(chm: Path, out_dir: Path) -> bool:
    """
    Windows only: use hh.exe to decompile CHM to HTML.
    """
    if platform.system().lower() != "windows":
        return False
    hh = Path(os.environ.get("WINDIR", r"C:\Windows")) / "hh.exe"
    if not hh.exists():
        return False
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [str(hh), "-decompile", str(out_dir), str(chm)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except Exception:
        return False


def _iter_spaceclaim_chm(spaceclaim_dir: Path, tmp_dir: Path) -> Iterator[DocChunk]:
    if not spaceclaim_dir.exists():
        return
    chms = sorted([p for p in spaceclaim_dir.rglob("*.chm") if p.is_file()])
    for chm in chms:
        title = chm.stem
        extracted = tmp_dir / "spaceclaim_chm" / chm.stem
        ok = _decompile_chm(chm, extracted)
        if not ok:
            yield DocChunk(
                source="spaceclaim_chm",
                title=title,
                locator=f"{chm.name}#NO_EXTRACT",
                path=str(chm),
                text="CHM extraction failed. On Windows, ensure hh.exe exists and run with sufficient permission.",
            )
            continue

        html_files = [p for p in extracted.rglob("*.htm*") if p.is_file()]
        for html in sorted(html_files):
            try:
                raw = html.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            parser = _HTMLText()
            try:
                parser.feed(raw)
            except Exception:
                continue
            text = parser.text()
            if not text:
                continue
            rel = str(html.relative_to(extracted)).replace("\\", "/")
            for idx, chunk in enumerate(_chunk_text(text), start=1):
                yield DocChunk(
                    source="spaceclaim_chm",
                    title=title,
                    locator=f"{chm.name}:{rel}#chunk{idx}",
                    path=str(html),
                    text=chunk,
                )


def _iter_plain_text(root: Path, *, source: str) -> Iterator[DocChunk]:
    """
    Index plain text artifacts placed under docs folders.
    Useful when CHM isn't available yet (e.g., api summary notes).
    """
    if not root.exists():
        return
    exts = {".txt", ".md"}
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts]
    for fp in sorted(files):
        title = fp.stem
        try:
            raw = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not raw.strip():
            continue
        rel = str(fp.relative_to(root)).replace("\\", "/")
        for idx, chunk in enumerate(_chunk_text(raw), start=1):
            yield DocChunk(
                source=source,
                title=title,
                locator=f"{rel}#chunk{idx}",
                path=str(fp),
                text=chunk,
            )


def _iter_pyansys_html(pyansys_dir: Path) -> Iterator[DocChunk]:
    if not pyansys_dir.exists():
        return
    html_files = [p for p in pyansys_dir.rglob("*.htm*") if p.is_file()]
    for html in sorted(html_files):
        try:
            raw = html.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        parser = _HTMLText()
        try:
            parser.feed(raw)
        except Exception:
            continue
        text = parser.text()
        if not text:
            continue
        title = html.stem
        rel = str(html.relative_to(pyansys_dir)).replace("\\", "/")
        for idx, chunk in enumerate(_chunk_text(text), start=1):
            yield DocChunk(
                source="pyansys_html",
                title=title,
                locator=f"{rel}#chunk{idx}",
                path=str(html),
                text=chunk,
            )


def _iter_pyansys_docstrings(pyansys_dir: Path) -> Iterator[DocChunk]:
    """
    Index JSONL dumps created by dump_docstrings.py.
    Expected line shape:
      { "module": "...", "qualname": "...", "kind": "...", "signature": "...", "doc": "..." }
    """
    if not pyansys_dir.exists():
        return
    jsonls = [p for p in pyansys_dir.rglob("*.jsonl") if p.is_file()]
    for jl in sorted(jsonls):
        try:
            lines = jl.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            doc = str(obj.get("doc", "")).strip()
            qual = str(obj.get("qualname", "")).strip()
            mod = str(obj.get("module", "")).strip()
            if not doc or not qual:
                continue
            title = qual
            locator = f"{jl.name}#L{i}"
            text = f"{qual}{(' ' + obj.get('signature','')) if obj.get('signature') else ''}\n\n{doc}"
            for idx, chunk in enumerate(_chunk_text(text), start=1):
                yield DocChunk(
                    source="pyansys_docstring",
                    title=title,
                    locator=f"{locator}-chunk{idx}",
                    path=str(jl),
                    text=chunk,
                )


def build_index(*, docs_root: Path, out_db: Path, reset: bool) -> int:
    ansys_dir = docs_root / "ansys"
    spaceclaim_dir = docs_root / "spaceclaim"
    pyansys_dir = docs_root / "pyansys"

    conn = _ensure_db(out_db, reset=reset)
    tmp_dir = out_db.parent / ".tmp_extract"

    total = 0
    total += _upsert_chunks(conn, _iter_ansys_pdf(ansys_dir))
    total += _upsert_chunks(conn, _iter_spaceclaim_chm(spaceclaim_dir, tmp_dir))
    total += _upsert_chunks(conn, _iter_plain_text(spaceclaim_dir, source="spaceclaim_text"))
    total += _upsert_chunks(conn, _iter_pyansys_html(pyansys_dir))
    total += _upsert_chunks(conn, _iter_pyansys_docstrings(pyansys_dir))
    total += _upsert_chunks(conn, _iter_plain_text(pyansys_dir, source="pyansys_text"))
    conn.close()
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs-root", required=True, help="root containing ansys/ spaceclaim/ pyansys/")
    ap.add_argument("--out", required=True, help="output sqlite db path")
    ap.add_argument("--reset", action="store_true", help="drop and rebuild db")
    args = ap.parse_args()

    docs_root = Path(args.docs_root)
    out_db = Path(args.out)
    n = build_index(docs_root=docs_root, out_db=out_db, reset=bool(args.reset))
    print(f"[ok] indexed chunks: {n}")
    print(f"[ok] db: {out_db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
