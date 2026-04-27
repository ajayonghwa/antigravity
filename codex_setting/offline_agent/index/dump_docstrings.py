#!/usr/bin/env python3
"""
Dump docstrings/type info from installed PyAnsys packages to JSONL for offline indexing.

Why:
- Web manuals are fragmented and version-skewed.
- Docstrings/type hints come from the exact versions installed on the offline machine.

Output:
- One JSON object per line (JSONL), with: module, qualname, kind, signature, doc.
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class DocItem:
    module: str
    qualname: str
    kind: str  # "function" | "class" | "method"
    signature: str
    doc: str


def _safe_sig(obj: Any) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception:
        return ""


def _safe_doc(obj: Any) -> str:
    try:
        return inspect.getdoc(obj) or ""
    except Exception:
        return ""


def _iter_public_items(mod: Any, *, max_items: int) -> list[DocItem]:
    out: list[DocItem] = []

    for name, obj in sorted(vars(mod).items(), key=lambda kv: kv[0]):
        if name.startswith("_"):
            continue

        if inspect.isfunction(obj):
            doc = _safe_doc(obj)
            if not doc:
                continue
            out.append(
                DocItem(
                    module=mod.__name__,
                    qualname=f"{mod.__name__}.{name}",
                    kind="function",
                    signature=_safe_sig(obj),
                    doc=doc,
                )
            )
        elif inspect.isclass(obj):
            doc = _safe_doc(obj)
            if doc:
                out.append(
                    DocItem(
                        module=mod.__name__,
                        qualname=f"{mod.__name__}.{name}",
                        kind="class",
                        signature=_safe_sig(getattr(obj, "__init__", obj)),
                        doc=doc,
                    )
                )

            # Also dump public methods (lightly)
            for m_name, m_obj in inspect.getmembers(obj):
                if m_name.startswith("_"):
                    continue
                if not (inspect.isfunction(m_obj) or inspect.ismethod(m_obj)):
                    continue
                m_doc = _safe_doc(m_obj)
                if not m_doc:
                    continue
                out.append(
                    DocItem(
                        module=mod.__name__,
                        qualname=f"{mod.__name__}.{name}.{m_name}",
                        kind="method",
                        signature=_safe_sig(m_obj),
                        doc=m_doc,
                    )
                )
                if len(out) >= max_items:
                    return out

        if len(out) >= max_items:
            return out

    return out


def dump_modules(*, modules: list[str], out_jsonl: Path, max_items: int) -> int:
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    written = 0

    with open(out_jsonl, "w", encoding="utf-8") as f:
        for m in modules:
            try:
                mod = importlib.import_module(m)
            except Exception as e:
                err = {"module": m, "error": f"import failed: {type(e).__name__}: {e}"}
                f.write(json.dumps(err, ensure_ascii=False) + "\n")
                continue

            items = _iter_public_items(mod, max_items=max_items)
            for it in items:
                f.write(json.dumps(asdict(it), ensure_ascii=False) + "\n")
                written += 1

    return written


def _split_csv(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--modules",
        default="ansys.dpf.core,ansys.mapdl.core",
        help="comma-separated module list to import and dump",
    )
    ap.add_argument("--out", default="pyansys_docstrings.jsonl", help="output JSONL path")
    ap.add_argument("--max-items", type=int, default=500, help="max items per module (soft limit)")
    args = ap.parse_args()

    modules = _split_csv(str(args.modules))
    out = Path(str(args.out))
    n = dump_modules(modules=modules, out_jsonl=out, max_items=int(args.max_items))
    print(f"[ok] wrote {n} doc items to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

