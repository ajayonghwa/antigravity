#!/usr/bin/env python3
"""
DPF 후처리 최소 템플릿 (에어갭 + 작은 로컬 LLM용)

목표:
- Workbench `*.rst`에서 결과를 "일단 안전하게" 읽어오는 골격을 고정한다.
- DPF API/버전 차이로 생길 수 있는 실패는 "지어내지 말고" 디스커버리 출력으로 좁힌다.

사용 예:
  python dpf_postprocess_template.py --rst "C:\\path\\file.rst" --analysis modal --mode 1 --results disp,stress --outdir out

주의:
- reaction force / stress linearization은 프로젝트/버전마다 스코핑과 연산자가 달라지기 쉬워서,
  우선은 "가능한 연산자/결과 이름 디스커버리" + "데이터 뽑아 CSV 저장"에 초점을 둔다.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional


@dataclass(frozen=True)
class ScopingSpec:
    location: str  # "nodal" | "elemental"
    ids: list[int]


def _load_scoping(path: Optional[str]) -> Optional[ScopingSpec]:
    if not path:
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    location = str(data.get("location", "")).strip().lower()
    ids_raw = data.get("ids", [])
    ids = [int(x) for x in ids_raw]
    if location not in {"nodal", "elemental"}:
        raise ValueError(f"scoping.location must be 'nodal' or 'elemental' (got {location!r})")
    if not ids:
        raise ValueError("scoping.ids must be a non-empty list of ints")
    return ScopingSpec(location=location, ids=ids)


def _ensure_outdir(outdir: str) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _as_rows(fields: Any) -> list[dict[str, Any]]:
    """
    DPF Fields/FieldsContainer -> row dict list (best-effort).
    - API가 환경마다 조금씩 달라서, 실패하면 호출자가 디스커버리 출력으로 보완한다.
    """
    rows: list[dict[str, Any]] = []

    # FieldsContainer: indexable, has labels maybe
    if hasattr(fields, "__len__") and hasattr(fields, "__getitem__") and not hasattr(fields, "data"):
        # take first field by default (caller can split per set later)
        try:
            field = fields[0]
        except Exception:
            field = fields
    else:
        field = fields

    # Field: has scoping + data
    if hasattr(field, "scoping") and hasattr(field, "data"):
        scoping = getattr(field, "scoping", None)
        ids = []
        if scoping is not None and hasattr(scoping, "ids"):
            try:
                ids = list(scoping.ids)
            except Exception:
                ids = []
        data = getattr(field, "data", None)
        try:
            data_list = data.tolist() if hasattr(data, "tolist") else list(data)
        except Exception:
            data_list = []

        for idx, v in enumerate(data_list):
            entity_id = ids[idx] if idx < len(ids) else None
            if isinstance(v, (list, tuple)) and len(v) in (3, 6, 9):
                row: dict[str, Any] = {"id": entity_id}
                for j, comp in enumerate(v):
                    row[f"c{j}"] = comp
                rows.append(row)
            else:
                rows.append({"id": entity_id, "value": v})
        return rows

    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for r in rows:
        for k in r.keys():
            if k not in fieldnames:
                fieldnames.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def _discover_results(model: Any) -> list[str]:
    try:
        names = dir(model.results)
    except Exception:
        return []
    out: list[str] = []
    for n in names:
        if n.startswith("_"):
            continue
        try:
            attr = getattr(model.results, n)
        except Exception:
            continue
        if callable(attr):
            out.append(n)
    return sorted(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rst", required=True, help="Workbench result file path (*.rst)")
    parser.add_argument("--analysis", choices=["static", "modal", "harmonic", "transient"], default="static")
    parser.add_argument(
        "--set-id",
        type=int,
        default=None,
        help="time/freq set id. Prefer --mode for modal analysis.",
    )
    parser.add_argument(
        "--mode",
        type=int,
        default=None,
        help="modal mode index (1..N). Alias for --set-id with extra safety checks.",
    )
    parser.add_argument("--results", default="disp,stress", help="comma-separated: disp,stress,rf")
    parser.add_argument("--scoping", default=None, help="path to scoping JSON: {location:'nodal'|'elemental', ids:[...]}")
    parser.add_argument("--outdir", default="out", help="output directory")
    args = parser.parse_args()

    rst_path = Path(args.rst)
    if not rst_path.exists():
        raise SystemExit(f"RST not found: {rst_path}")

    requested = [x.strip().lower() for x in args.results.split(",") if x.strip()]
    scoping_spec = _load_scoping(args.scoping)
    outdir = _ensure_outdir(args.outdir)

    try:
        import ansys.dpf.core as dpf  # type: ignore
    except Exception as e:
        raise SystemExit(
            "Missing dependency: ansys.dpf.core. Install the matching offline wheel bundle for your environment."
        ) from e

    model = dpf.Model(str(rst_path))
    print(f"[info] loaded rst: {rst_path}")

    # Metadata discovery (best-effort)
    try:
        print(f"[info] dpf server: {dpf.SERVER_VERSION}")
    except Exception:
        pass

    try:
        mesh = model.metadata.meshed_region
        print(f"[info] mesh nodes: {mesh.nodes.n_nodes} | elements: {mesh.elements.n_elements}")
    except Exception:
        pass

    # Mode selection safety: prefer explicit --mode for modal to avoid ambiguity.
    if args.mode is not None and args.set_id is not None and args.mode != args.set_id:
        print("[need] conflicting inputs: --mode and --set-id differ. Use only one.")
        return 2
    if args.mode is not None:
        args.set_id = int(args.mode)

    # If set_id is missing for modal/harmonic/transient, force explicitness to avoid silent wrong answers.
    if args.analysis in {"modal", "harmonic", "transient"} and args.set_id is None:
        if args.analysis == "modal":
            print("[need] --mode is required for modal analysis to avoid wrong mode selection.")
            print("[hint] Use --mode 1 (or 2, 3, ...) for the target eigenmode index.")
        else:
            print("[need] --set-id is required for analysis in {harmonic,transient} to avoid wrong set selection.")
        return 2

    if args.analysis == "modal" and args.set_id is not None and int(args.set_id) <= 0:
        print("[need] --mode must be >= 1 for modal analysis.")
        return 2

    # Time/freq scoping
    time_scoping = None
    if args.set_id is not None:
        try:
            time_scoping = dpf.time_freq_scoping_factory.scoping([int(args.set_id)])
        except Exception:
            time_scoping = None

    # Scoping (optional)
    dpf_scoping = None
    if scoping_spec is not None:
        try:
            if scoping_spec.location == "nodal":
                dpf_scoping = dpf.mesh_scoping_factory.nodal_scoping(scoping_spec.ids)
            else:
                dpf_scoping = dpf.mesh_scoping_factory.elemental_scoping(scoping_spec.ids)
        except Exception:
            dpf_scoping = None

    # Results discovery: print available result builders so the user can map rf/stress names per version.
    avail = _discover_results(model)
    if avail:
        print("[discover] model.results methods (sample):")
        print("  " + ", ".join(avail[:60]) + (" ..." if len(avail) > 60 else ""))

    def eval_result(builder_name: str, out_name: str) -> None:
        builder = getattr(model.results, builder_name, None)
        if builder is None or not callable(builder):
            print(f"[skip] result builder not found: model.results.{builder_name}()")
            return

        kwargs = {}
        # Many DPF result builders accept time_scoping / mesh_scoping. We pass only when we have it.
        if time_scoping is not None:
            kwargs["time_scoping"] = time_scoping
        if dpf_scoping is not None:
            kwargs["mesh_scoping"] = dpf_scoping

        res = builder(**kwargs) if kwargs else builder()
        if not hasattr(res, "eval"):
            print(f"[skip] result object has no eval(): {builder_name}")
            return
        fc = res.eval()
        rows = _as_rows(fc)
        out_path = outdir / out_name
        _write_csv(out_path, rows)
        print(f"[ok] wrote {out_path} ({len(rows)} rows)")

    # Minimal safe mappings (best-effort). If these names differ in your DPF version,
    # use the [discover] output and update builder_name.
    if "disp" in requested:
        eval_result("displacement", "displacement.csv")
    if "stress" in requested:
        eval_result("stress", "stress.csv")
    if "rf" in requested:
        # Many environments differ here (reaction_force, nodal_reaction_force, etc.)
        # We default to a common guess but will not die if missing.
        eval_result("reaction_force", "reaction_force.csv")

    print("[done] if a result is missing, copy the [discover] list and pick the correct builder name for your version.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
