#!/usr/bin/env python3
"""
Fetch top-k evidence chunks from the local docs index for use in an LLM prompt.

This is the "glue" between:
  - your offline index (SQLite FTS)
  - your local LLM agent (Cline / Continue / etc.)

Typical workflow (offline, Windows):
  1) Build index once (run_build_index.bat)
  2) For each coding task, run:
       py -3.10 offline_agent\\rag\\get_context.py --db D:\\index\\docs_index.sqlite --q "MassProperties inertia tensor" --k 6
  3) Paste the output into the agent prompt under a "SOURCES" section.

Design:
  - Output is *prompt-ready* markdown.
  - Includes chunk_id so you can cite sources and re-fetch exact chunks later.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def _connect(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def fetch(conn: sqlite3.Connection, q: str, k: int) -> list[dict[str, str]]:
    rows = conn.execute(
        """
        SELECT c.chunk_id, c.source, c.title, c.locator, c.path, c.text
        FROM chunks_fts f
        JOIN chunks c ON c.rowid = f.rowid
        WHERE chunks_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (q, k),
    ).fetchall()
    return [dict(r) for r in rows]


def clip(s: str, n: int) -> str:
    s = (s or "").strip()
    if len(s) <= n:
        return s
    return s[:n].rstrip() + "\n...[clipped]..."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="docs_index.sqlite path")
    ap.add_argument("--q", required=True, help="FTS query string")
    ap.add_argument("--k", type=int, default=6, help="top-k chunks")
    ap.add_argument("--max-chars", type=int, default=1800, help="max chars per chunk in output")
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        print(f"[err] db not found: {db}")
        return 2

    conn = _connect(db)
    hits = fetch(conn, args.q, int(args.k))
    conn.close()

    if not hits:
        print("# SOURCES\n\n(no matches)\n")
        print("## Next action\n- Refine the query using exact API names / keywords from the error message.\n")
        return 0

    print("# SOURCES\n")
    for i, h in enumerate(hits, start=1):
        chunk_id = h.get("chunk_id", "")
        source = h.get("source", "")
        title = h.get("title", "") or ""
        locator = h.get("locator", "") or ""
        path = h.get("path", "") or ""
        text = clip(h.get("text", "") or "", int(args.max_chars))

        print(f"## Source {i}")
        print(f"- chunk_id: `{chunk_id}`")
        print(f"- source: `{source}`")
        if title:
            print(f"- title: `{title}`")
        if locator:
            print(f"- locator: `{locator}`")
        if path:
            print(f"- path: `{path}`")
        print("")
        print("```text")
        print(text)
        print("```")
        print("")

    print("## Rules for the agent")
    print("- Use only these sources for API names/signatures/keywords. If missing, ask for a better query.")
    print("- When you output code, include the cited `chunk_id`(s) you relied on.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

