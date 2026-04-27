#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def search(db: Path, q: str, *, limit: int) -> list[dict[str, str]]:
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT chunk_id, source, title, locator, path,
               snippet(chunks_fts, 5, '[', ']', '…', 12) AS snip
        FROM chunks_fts
        WHERE chunks_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (q, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--q", required=True)
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        print(f"[err] db not found: {db}")
        return 2

    hits = search(db, args.q, limit=int(args.limit))
    if not hits:
        print("[none] no results")
        return 0

    for h in hits:
        print("")
        print(f"chunk_id: {h['chunk_id']}")
        print(f"source:   {h['source']}")
        print(f"title:    {h.get('title') or ''}")
        print(f"locator:  {h.get('locator') or ''}")
        print(f"path:     {h.get('path') or ''}")
        print(f"snippet:  {h.get('snip') or ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

