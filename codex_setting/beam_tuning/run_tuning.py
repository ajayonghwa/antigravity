#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class Segment:
    segment_id: str
    mass: Optional[float]
    cog: tuple[Optional[float], Optional[float], Optional[float]]
    inertia_cog: tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]
    feature_type: str
    od: tuple[Optional[float], Optional[float], Optional[float]]  # (min, val, max)
    id: tuple[Optional[float], Optional[float], Optional[float]]
    thk: tuple[Optional[float], Optional[float], Optional[float]]
    length: tuple[Optional[float], Optional[float], Optional[float]]
    notes: str


@dataclass(frozen=True)
class Target:
    mode: int
    freq_hz: Optional[float]
    eff_mass: tuple[Optional[float], Optional[float], Optional[float]]  # x,y,z
    w_freq: float
    w_mass: float


@dataclass(frozen=True)
class Connector:
    connector_id: str
    kind: str  # combin14 | combin39 | mass21 | ce | cp | d | rbe3
    from_segment: Optional[str]
    to_segment: Optional[str]
    dof: Optional[str]  # UX, UY, UZ, ROTX, ROTY, ROTZ (convention depends on your standard)
    k: tuple[Optional[float], Optional[float], Optional[float]]  # min,val,max
    c: tuple[Optional[float], Optional[float], Optional[float]]  # min,val,max
    mass_kg: Optional[float]
    notes: str


def _f(s: str) -> Optional[float]:
    s = (s or "").strip()
    if not s:
        return None
    return float(s)


def _i(s: str) -> int:
    return int((s or "").strip())


def load_segments(path: Path) -> list[Segment]:
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        out: list[Segment] = []
        for row in r:
            seg_id = (row.get("segment_id") or "").strip()
            if not seg_id:
                continue
            out.append(
                Segment(
                    segment_id=seg_id,
                    mass=_f(row.get("mass", "")),
                    cog=(_f(row.get("cog_x", "")), _f(row.get("cog_y", "")), _f(row.get("cog_z", ""))),
                    inertia_cog=(
                        _f(row.get("Ixx_cog", "")),
                        _f(row.get("Iyy_cog", "")),
                        _f(row.get("Izz_cog", "")),
                        _f(row.get("Ixy_cog", "")),
                        _f(row.get("Iyz_cog", "")),
                        _f(row.get("Izx_cog", "")),
                    ),
                    feature_type=(row.get("feature_type") or "unknown").strip() or "unknown",
                    od=(_f(row.get("od_min", "")), _f(row.get("od", "")), _f(row.get("od_max", ""))),
                    id=(_f(row.get("id_min", "")), _f(row.get("id", "")), _f(row.get("id_max", ""))),
                    thk=(_f(row.get("thk_min", "")), _f(row.get("thk", "")), _f(row.get("thk_max", ""))),
                    length=(_f(row.get("len_min", "")), _f(row.get("len", "")), _f(row.get("len_max", ""))),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return out


def load_targets(path: Path) -> list[Target]:
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        out: list[Target] = []
        for row in r:
            mode_s = (row.get("mode") or "").strip()
            if not mode_s:
                continue
            out.append(
                Target(
                    mode=_i(mode_s),
                    freq_hz=_f(row.get("frequency_hz_target", "")),
                    eff_mass=(
                        _f(row.get("eff_mass_x_target", "")),
                        _f(row.get("eff_mass_y_target", "")),
                        _f(row.get("eff_mass_z_target", "")),
                    ),
                    w_freq=float((row.get("weight_freq") or "1.0").strip() or "1.0"),
                    w_mass=float((row.get("weight_mass") or "1.0").strip() or "1.0"),
                )
            )
    return out


def load_connectors(path: Optional[Path]) -> list[Connector]:
    if path is None:
        return []
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        out: list[Connector] = []
        for row in r:
            cid = (row.get("connector_id") or "").strip()
            if not cid:
                continue
            kind = (row.get("kind") or "").strip().lower()
            out.append(
                Connector(
                    connector_id=cid,
                    kind=kind or "unknown",
                    from_segment=(row.get("from_segment") or "").strip() or None,
                    to_segment=(row.get("to_segment") or "").strip() or None,
                    dof=(row.get("dof") or "").strip() or None,
                    k=(_f(row.get("k_min", "")), _f(row.get("k", "")), _f(row.get("k_max", ""))),
                    c=(_f(row.get("c_min", "")), _f(row.get("c", "")), _f(row.get("c_max", ""))),
                    mass_kg=_f(row.get("mass_kg", "")),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return out


def write_apdl_template(outdir: Path, segments: list[Segment], connectors: list[Connector]) -> Path:
    """
    Generates an APDL template with placeholders.
    The *actual* element definitions/sections depend on your modeling standard.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    apdl = outdir / "beam_model_template.mac"
    lines: list[str] = []
    lines.append("! Beam/Shell model template (generated)")
    lines.append("! NOTE: Fill in element types, sections, and connectivity per your standard.")
    lines.append("! Common element palette (by user): BEAM188, SHELL181; sometimes COMBIN14/39, MASS21, CE/CP/D, RBE3-like constraints.")
    lines.append("! Guardrail: modal analysis only")
    lines.append("/PREP7")
    lines.append("! --- MATERIAL (example) ---")
    lines.append("! MP,EX,1,<E>")
    lines.append("! MP,PRXY,1,<nu>   ! IMPORTANT: poisson uses PRXY")
    lines.append("! MP,DENS,1,<rho>")
    lines.append("! --- GEOMETRY PARAMS (from segments csv) ---")
    for s in segments:
        lines.append(f"! segment {s.segment_id}: feature={s.feature_type} od={s.od} id={s.id} thk={s.thk} len={s.length}")
    if connectors:
        lines.append("! --- CONNECTORS / CONSTRAINTS (from connectors csv) ---")
        lines.append("! IMPORTANT: Do not guess APDL syntax. Implement each item using your APDL manual / standard.")
        for c in connectors:
            lines.append(
                f"! connector {c.connector_id}: kind={c.kind} from={c.from_segment} to={c.to_segment} dof={c.dof} "
                f"k={c.k} c={c.c} mass_kg={c.mass_kg} notes={c.notes}"
            )
    lines.append("! --- SOLUTION (modal only) ---")
    lines.append("/SOLU")
    lines.append("ANTYPE,MODAL")
    lines.append("! MODOPT,LANB,<NMODES>")
    lines.append("! MXPAND,<NMODES>,,,YES")
    lines.append("SOLVE")
    lines.append("FINISH")
    apdl.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return apdl


def write_user_fill_csv(outdir: Path, segments: list[Segment]) -> Path:
    """
    Writes a CSV with "fill-me" blanks aligned to the segment schema.
    This is useful when SpaceClaim output doesn't contain all fields you want.
    """
    p = outdir / "segments_fill_me.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "segment_id",
                "mass",
                "cog_x",
                "cog_y",
                "cog_z",
                "Ixx_cog",
                "Iyy_cog",
                "Izz_cog",
                "Ixy_cog",
                "Iyz_cog",
                "Izx_cog",
                "feature_type",
                "od_min",
                "od",
                "od_max",
                "id_min",
                "id",
                "id_max",
                "thk_min",
                "thk",
                "thk_max",
                "len_min",
                "len",
                "len_max",
                "notes",
            ],
        )
        w.writeheader()
        for s in segments:
            w.writerow(
                {
                    "segment_id": s.segment_id,
                    "mass": s.mass or "",
                    "cog_x": s.cog[0] or "",
                    "cog_y": s.cog[1] or "",
                    "cog_z": s.cog[2] or "",
                    "Ixx_cog": s.inertia_cog[0] or "",
                    "Iyy_cog": s.inertia_cog[1] or "",
                    "Izz_cog": s.inertia_cog[2] or "",
                    "Ixy_cog": s.inertia_cog[3] or "",
                    "Iyz_cog": s.inertia_cog[4] or "",
                    "Izx_cog": s.inertia_cog[5] or "",
                    "feature_type": s.feature_type,
                    "od_min": s.od[0] or "",
                    "od": s.od[1] or "",
                    "od_max": s.od[2] or "",
                    "id_min": s.id[0] or "",
                    "id": s.id[1] or "",
                    "id_max": s.id[2] or "",
                    "thk_min": s.thk[0] or "",
                    "thk": s.thk[1] or "",
                    "thk_max": s.thk[2] or "",
                    "len_min": s.length[0] or "",
                    "len": s.length[1] or "",
                    "len_max": s.length[2] or "",
                    "notes": s.notes,
                }
            )
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--connectors", default=None, help="optional connectors CSV (combin/mass/constraints)")
    ap.add_argument(
        "--tuning-mode",
        default="basic",
        choices=["basic", "mac"],
        help="basic: freq+effective-mass. mac: also includes mode-shape MAC (requires DPF mode shapes + mapping).",
    )
    ap.add_argument("--outdir", default="out")
    args = ap.parse_args()

    segments = load_segments(Path(args.segments))
    targets = load_targets(Path(args.targets))
    connectors = load_connectors(Path(args.connectors)) if args.connectors else []
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Basic validation (fail-fast)
    if not segments:
        raise SystemExit("No segments loaded")
    if not targets:
        raise SystemExit("No targets loaded")

    # Emit a machine-readable snapshot for the agent loop
    (outdir / "segments.json").write_text(json.dumps([s.__dict__ for s in segments], ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    (outdir / "targets.json").write_text(json.dumps([t.__dict__ for t in targets], ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    (outdir / "connectors.json").write_text(
        json.dumps([c.__dict__ for c in connectors], ensure_ascii=False, default=str, indent=2), encoding="utf-8"
    )

    apdl = write_apdl_template(outdir, segments, connectors)
    fill_me = write_user_fill_csv(outdir, segments)
    print(f"[ok] wrote: {apdl}")
    print(f"[ok] wrote: {fill_me}")
    print(f"[info] tuning_mode: {args.tuning_mode}")

    # We intentionally do not implement auto-update tuning loop here yet.
    # The correct implementation depends on:
    # - how you run MAPDL (ansys.mapdl.core vs manual)
    # - where you read modal frequencies/effective mass from
    # - whether MAC uses solid model shapes and how DOFs are mapped
    if args.tuning_mode == "basic":
        print("[next] Implement objective: frequency + directional effective mass (basic).")
    else:
        print("[next] Implement objective: basic + MAC(model, solid) (advanced). Requires DPF mode-shape extraction.")

    print("[next] Hook this into your MAPDL execution environment (ansys.mapdl.core or manual run).")
    print("[next] Add objective function: freq + effective mass (+ optional MAC) once result extraction is confirmed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
