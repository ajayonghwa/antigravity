#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class BeamEdge:
    beam_id: str
    segment_id: str
    node_start_id: int
    node_end_id: int
    start: tuple[float, float, float]
    end: tuple[float, float, float]
    insert_axis: str  # x|y|z
    insert_positions: list[float]  # coordinates along axis
    notes: str


@dataclass(frozen=True)
class NodeSpec:
    node_id: int
    segment_id: str
    x: float
    y: float
    z: float
    notes: str


def _f(s: str) -> float:
    return float((s or "").strip())


def _i(s: str) -> int:
    return int((s or "").strip())


def _split_positions(s: str) -> list[float]:
    s = (s or "").strip()
    if not s:
        return []
    parts = []
    for token in s.replace(",", ";").split(";"):
        t = token.strip()
        if not t:
            continue
        parts.append(float(t))
    # unique + sorted
    return sorted(set(parts))


def load_beams(path: Path) -> list[BeamEdge]:
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        out: list[BeamEdge] = []
        for row in r:
            bid = (row.get("beam_id") or "").strip()
            if not bid:
                continue
            axis = (row.get("insert_axis") or "z").strip().lower()
            out.append(
                BeamEdge(
                    beam_id=bid,
                    segment_id=(row.get("segment_id") or "").strip(),
                    node_start_id=_i(row.get("node_start_id") or "0"),
                    node_end_id=_i(row.get("node_end_id") or "0"),
                    start=(_f(row.get("x_start") or "0"), _f(row.get("y_start") or "0"), _f(row.get("z_start") or "0")),
                    end=(_f(row.get("x_end") or "0"), _f(row.get("y_end") or "0"), _f(row.get("z_end") or "0")),
                    insert_axis=axis,
                    insert_positions=_split_positions(row.get("insert_positions") or ""),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return out


_NODE_RE = re.compile(r"^\s*N\s*,\s*(\d+)\s*,", re.IGNORECASE)


def scan_max_node_id(apdl_path: Path) -> int:
    """
    Best-effort scan for max node id from an APDL text file containing `N,<id>,x,y,z` lines.
    Ignores comment lines starting with `!`.
    """
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


def _interp(start: tuple[float, float, float], end: tuple[float, float, float], t: float) -> tuple[float, float, float]:
    return (start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t, start[2] + (end[2] - start[2]) * t)


def split_beam(edge: BeamEdge, *, next_node_id: int) -> tuple[list[NodeSpec], list[tuple[int, int]], int]:
    """
    Returns:
    - inserted nodes
    - new connectivity list (node_id pairs) in order from start->end
    - updated next_node_id

    Assumptions:
    - insertion is specified by a single axis coordinate (x OR y OR z)
    - start/end axis values define a line. Positions outside [min,max] are ignored.
    """
    sx, sy, sz = edge.start
    ex, ey, ez = edge.end
    axis = edge.insert_axis
    if axis not in {"x", "y", "z"}:
        raise ValueError(f"insert_axis must be x|y|z (got {axis!r})")

    a0 = {"x": sx, "y": sy, "z": sz}[axis]
    a1 = {"x": ex, "y": ey, "z": ez}[axis]
    if a0 == a1:
        # degenerate on that axis; cannot place
        return ([], [(edge.node_start_id, edge.node_end_id)], next_node_id)

    lo = min(a0, a1)
    hi = max(a0, a1)
    positions = [p for p in edge.insert_positions if lo < p < hi]
    if not positions:
        return ([], [(edge.node_start_id, edge.node_end_id)], next_node_id)

    inserted: list[NodeSpec] = []
    # order positions along start->end direction
    forward = a1 > a0
    positions_sorted = sorted(positions, reverse=not forward)

    for p in positions_sorted:
        t = (p - a0) / (a1 - a0)
        x, y, z = _interp(edge.start, edge.end, t)
        inserted.append(
            NodeSpec(
                node_id=next_node_id,
                segment_id=edge.segment_id,
                x=x,
                y=y,
                z=z,
                notes=f"inserted on beam {edge.beam_id} at {axis}={p}",
            )
        )
        next_node_id += 1

    chain = [edge.node_start_id] + [n.node_id for n in inserted] + [edge.node_end_id]
    connectivity = list(zip(chain[:-1], chain[1:]))
    return (inserted, connectivity, next_node_id)


def write_nodes_csv(path: Path, nodes: list[NodeSpec]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["node_id", "segment_id", "x", "y", "z", "notes"])
        w.writeheader()
        for n in nodes:
            w.writerow({"node_id": n.node_id, "segment_id": n.segment_id, "x": n.x, "y": n.y, "z": n.z, "notes": n.notes})


def write_beams_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_apdl_macro(path: Path, inserted_nodes: list[NodeSpec], beam_splits: list[dict[str, str]]) -> None:
    """
    Emits an APDL macro skeleton:
    - N commands for inserted nodes (safe)
    - Element split section as TODO (avoid guessing element attribute carry-over)
    """
    lines: list[str] = []
    lines.append("! split_beams.mac (generated)")
    lines.append("! Creates inserted nodes, and provides TODO blocks for splitting BEAM188/SHELL181 connectivity.")
    lines.append("! IMPORTANT: Do not guess how to copy element attributes/sections. Use your APDL manual/standard.")
    lines.append("")
    lines.append("/PREP7")
    lines.append("! --- INSERTED NODES ---")
    for n in inserted_nodes:
        lines.append(f"! {n.notes}")
        lines.append(f"N,{n.node_id},{n.x},{n.y},{n.z}")
    lines.append("")
    lines.append("! --- BEAM SPLIT TODO ---")
    lines.append("! For each original beam, delete/replace the element(s) between endpoints as appropriate, then create new elements.")
    for s in beam_splits:
        lines.append(
            f"! beam_id={s['beam_id']} original=({s['node_start_id']},{s['node_end_id']}) new_pairs={s['new_pairs']} notes={s['notes']}"
        )
        lines.append("! TODO: EDELE,<old_elem_id>   (if you identify element IDs)")
        lines.append("! TODO: E,<n1>,<n2> for each pair in new_pairs, with correct TYPE/MAT/SECNUM/REAL/ESYS")
    lines.append("FINISH")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--beams", required=True, help="beams CSV path")
    ap.add_argument("--outdir", default="out", help="output dir")
    ap.add_argument(
        "--node-id-start",
        default="auto",
        help="starting node id for inserted nodes. Use an int, or 'auto' to use (max node in --scan-apdl + offset).",
    )
    ap.add_argument("--scan-apdl", default=None, help="APDL file to scan for max existing node id (for auto start)")
    ap.add_argument("--node-id-offset", type=int, default=10, help="offset added to scanned max node id (auto mode)")
    ap.add_argument("--emit-apdl", action="store_true", help="also emit split_beams.mac skeleton")
    args = ap.parse_args()

    beams = load_beams(Path(args.beams))
    if not beams:
        raise SystemExit("No beams loaded")

    if str(args.node_id_start).strip().lower() == "auto":
        if not args.scan_apdl:
            raise SystemExit("--node-id-start auto requires --scan-apdl <apdl-file>")
        max_id = scan_max_node_id(Path(args.scan_apdl))
        next_id = int(max_id) + int(args.node_id_offset)
    else:
        next_id = int(str(args.node_id_start).strip())
    inserted_all: list[NodeSpec] = []
    beam_splits: list[dict[str, str]] = []

    for b in beams:
        inserted, conn, next_id = split_beam(b, next_node_id=next_id)
        inserted_all.extend(inserted)
        pairs_str = "|".join([f"{a}-{c}" for a, c in conn])
        beam_splits.append(
            {
                "beam_id": b.beam_id,
                "segment_id": b.segment_id,
                "node_start_id": str(b.node_start_id),
                "node_end_id": str(b.node_end_id),
                "new_pairs": pairs_str,
                "notes": b.notes,
            }
        )

    outdir = Path(args.outdir)
    write_nodes_csv(outdir / "inserted_nodes.csv", inserted_all)
    write_beams_csv(outdir / "beam_splits.csv", beam_splits)
    if args.emit_apdl:
        write_apdl_macro(outdir / "split_beams.mac", inserted_all, beam_splits)

    print(f"[ok] inserted_nodes: {len(inserted_all)} -> {outdir / 'inserted_nodes.csv'}")
    print(f"[ok] beam_splits: {len(beam_splits)} -> {outdir / 'beam_splits.csv'}")
    if args.emit_apdl:
        print(f"[ok] apdl skeleton -> {outdir / 'split_beams.mac'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
