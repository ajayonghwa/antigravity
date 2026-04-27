#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class NodeSpec:
    node_id: Optional[int]
    segment_id: str
    x: float
    y: float
    z: float
    shared_key: str
    share_mode: str  # shared | isolated
    attach_kind: str  # cp | ce | rbe3 | d | none
    attach_dofs: str
    notes: str


def load_nodes(path: Path) -> list[NodeSpec]:
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        out: list[NodeSpec] = []
        for row in r:
            node_id_s = (row.get("node_id") or "").strip()
            seg_id = (row.get("segment_id") or "").strip()
            if not seg_id:
                continue
            out.append(
                NodeSpec(
                    node_id=int(node_id_s) if node_id_s else None,
                    segment_id=seg_id,
                    x=float((row.get("x") or "0").strip() or "0"),
                    y=float((row.get("y") or "0").strip() or "0"),
                    z=float((row.get("z") or "0").strip() or "0"),
                    shared_key=(row.get("shared_key") or "").strip(),
                    share_mode=((row.get("share_mode") or "isolated").strip().lower() or "isolated"),
                    attach_kind=((row.get("attach_kind") or "none").strip().lower() or "none"),
                    attach_dofs=(row.get("attach_dofs") or "").strip(),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return out


_NODE_RE = re.compile(r"^\s*N\s*,\s*(\d+)\s*,", re.IGNORECASE)


def scan_max_node_id(apdl_path: Path) -> int:
    try:
        lines = apdl_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return 0
    max_id = 0
    for line in lines:
        if not line:
            continue
        if line.lstrip().startswith("!"):
            continue
        m = _NODE_RE.match(line)
        if not m:
            continue
        try:
            nid = int(m.group(1))
        except Exception:
            continue
        if nid > max_id:
            max_id = nid
    return max_id


def allocate_node_ids(nodes: list[NodeSpec], *, start_id: int) -> list[NodeSpec]:
    next_id = start_id
    out: list[NodeSpec] = []
    for n in nodes:
        if n.node_id is None:
            out.append(NodeSpec(node_id=next_id, **{k: getattr(n, k) for k in n.__dataclass_fields__ if k != "node_id"}))
            next_id += 1
        else:
            out.append(n)
    return out


def write_apdl_macro(out_path: Path, nodes: list[NodeSpec]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("! add_nodes.mac (generated)")
    lines.append("! Purpose: add connection/reference nodes AFTER tuning, without changing element parameters.")
    lines.append("! IMPORTANT: Node numbering is explicit from CSV to avoid collisions with existing node IDs.")
    lines.append("! IMPORTANT: Do not guess constraint syntax. Use your APDL manual/standard for CP/CE/RBE3-like connections.")
    lines.append("")
    lines.append("/PREP7")

    # Create nodes
    lines.append("! --- NODE CREATION ---")
    for n in nodes:
        if n.node_id is None:
            raise RuntimeError("node_id missing after allocation")
        lines.append(f"! segment={n.segment_id} share_mode={n.share_mode} shared_key={n.shared_key} attach={n.attach_kind} dofs={n.attach_dofs} notes={n.notes}")
        lines.append(f"N,{n.node_id},{n.x},{n.y},{n.z}")

    # Connection placeholders grouped by shared_key
    lines.append("")
    lines.append("! --- ATTACHMENT PLACEHOLDERS ---")
    lines.append("! You typically attach these nodes to existing structure nodes/elements via CP/CE/constraint elements.")
    lines.append("! For shared nodes: shared_key groups nodes intended to represent the same physical point across segments.")
    lines.append("! For isolated nodes: treat them as segment-local connection points.")
    for n in nodes:
        if n.attach_kind == "none":
            continue
        if n.attach_kind in {"cp", "ce", "rbe3", "d"}:
            lines.append(f"! TODO({n.attach_kind}): attach node {n.node_id} (segment {n.segment_id}) dofs={n.attach_dofs} shared_key={n.shared_key}")
        else:
            lines.append(f"! TODO: unknown attach_kind={n.attach_kind} for node {n.node_id}")

    lines.append("FINISH")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nodes", required=True, help="nodes CSV path")
    ap.add_argument("--out", default="out/add_nodes.mac", help="output APDL macro path")
    ap.add_argument("--scan-apdl", default=None, help="optional APDL file to scan for max existing node id")
    ap.add_argument("--node-id-offset", type=int, default=10, help="offset added to scanned max node id (auto allocate)")
    ap.add_argument(
        "--node-id-start",
        default=None,
        help="optional explicit start node id for auto allocation (used when node_id field is blank)",
    )
    args = ap.parse_args()

    nodes = load_nodes(Path(args.nodes))
    if not nodes:
        raise SystemExit("No nodes loaded from CSV")

    needs_alloc = any(n.node_id is None for n in nodes)
    if needs_alloc:
        if args.node_id_start is not None:
            start_id = int(str(args.node_id_start).strip())
        elif args.scan_apdl:
            max_id = scan_max_node_id(Path(args.scan_apdl))
            start_id = int(max_id) + int(args.node_id_offset)
        else:
            raise SystemExit("Some node_id cells are blank. Provide --node-id-start or --scan-apdl for auto allocation.")
        nodes = allocate_node_ids(nodes, start_id=start_id)

    write_apdl_macro(Path(args.out), nodes)
    print(f"[ok] wrote: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
