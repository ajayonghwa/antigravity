#!/usr/bin/env python3
"""
SpaceClaim 내부 실행 스크립트 템플릿 (구조/입출력만 고정)

주의:
- 이 파일은 SpaceClaim API를 "지어내지" 않기 위한 템플릿이다.
- 실제 API 호출(선택 가져오기, 질량특성 계산, 치수 측정)은 반드시
  SpaceClaim CHM에서 근거를 발췌한 뒤 그 근거에 맞춰 채워 넣는다.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class MassProps:
    mass: float
    cog_x: float
    cog_y: float
    cog_z: float
    ixx: float
    iyy: float
    izz: float
    ixy: float
    iyz: float
    izx: float


@dataclass(frozen=True)
class Feature:
    feature_type: str  # "cylinder" | "disk" | "unknown"
    params: dict[str, Any]
    estimated: bool = True


@dataclass(frozen=True)
class AxisRange:
    """
    1-axis coordinate window in the active coordinate system.
    Units are assumed to match the document (e.g. mm).
    """

    axis: str  # "x" | "y" | "z"
    min: float
    max: float


def inertia_about_cog(
    *,
    inertia_about_origin: tuple[float, float, float, float, float, float],
    mass: float,
    cog: tuple[float, float, float],
) -> tuple[float, float, float, float, float, float]:
    """
    Parallel Axis Theorem (3D) to shift inertia tensor from origin to center of mass.

    Inputs:
    - inertia_about_origin: (Ixx, Iyy, Izz, Ixy, Iyz, Izx) about the global origin
    - mass: mass
    - cog: (x, y, z) of center of gravity in same coordinate system

    Output:
    - inertia_about_cog: (Ixx, Iyy, Izz, Ixy, Iyz, Izx)

    Note:
    - Sign conventions for products of inertia can differ by API. This function
      assumes the conventional inertia tensor:
        [ Ixx  -Ixy  -Izx ]
        [ -Ixy  Iyy  -Iyz ]
        [ -Izx  -Iyz  Izz ]
      If SpaceClaim reports different conventions, adjust with CHM evidence.
    """
    ixx_o, iyy_o, izz_o, ixy_o, iyz_o, izx_o = inertia_about_origin
    x, y, z = cog

    ixx_c = ixx_o - mass * (y * y + z * z)
    iyy_c = iyy_o - mass * (x * x + z * z)
    izz_c = izz_o - mass * (x * x + y * y)

    # Products of inertia shift:
    ixy_c = ixy_o + mass * x * y
    iyz_c = iyz_o + mass * y * z
    izx_c = izx_o + mass * z * x

    return (ixx_c, iyy_c, izz_c, ixy_c, iyz_c, izx_c)


def write_csv_row(path: str, *, segment_id: str, props: MassProps, feature: Feature) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    file_exists = p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "segment_id",
                "mass",
                "cog_x",
                "cog_y",
                "cog_z",
                "Ixx",
                "Iyy",
                "Izz",
                "Ixy",
                "Iyz",
                "Izx",
                "feature_type",
                "feature_params",
                "estimated",
            ],
        )
        if not file_exists:
            w.writeheader()
        w.writerow(
            {
                "segment_id": segment_id,
                "mass": props.mass,
                "cog_x": props.cog_x,
                "cog_y": props.cog_y,
                "cog_z": props.cog_z,
                "Ixx": props.ixx,
                "Iyy": props.iyy,
                "Izz": props.izz,
                "Ixy": props.ixy,
                "Iyz": props.iyz,
                "Izx": props.izx,
                "feature_type": feature.feature_type,
                "feature_params": json.dumps(feature.params, ensure_ascii=False),
                "estimated": feature.estimated,
            }
        )


def main() -> None:
    # TODO: 사용자가 채우는 설정(에이전트가 프롬프트에서 요구)
    out_csv = r"C:\temp\spaceclaim_props.csv"
    # Selection mode (choose exactly one)
    use_current_selection = True
    named_group: Optional[str] = None
    ranges: list[AxisRange] = []  # 예: [AxisRange(axis="z", min=100, max=250), AxisRange(axis="z", min=400, max=520)]

    # Reset output file for this run
    p = Path(out_csv)
    if p.exists():
        p.unlink()

    if sum(
        [
            1 if use_current_selection else 0,
            1 if named_group else 0,
            1 if ranges else 0,
        ]
    ) != 1:
        raise RuntimeError("Choose exactly one selection mode: current selection OR named_group OR ranges")

    # TODO: SpaceClaim API 근거(CHM 토픽)로 아래 3개를 구현
    # 1) 선택/영역 객체 구하기
    # - region = get_region_from_selection(...)
    # - region = get_region_by_name(named_group)
    # - regions = [get_region_by_range(r) for r in ranges]  # "잘라내서 선택"은 CHM 근거가 있을 때만 수행
    #
    # "좌표 범위" 모드는 권장 동작:
    # - 1차: bounding box 교차로 후보 바디를 선택
    # - 2차(가능할 때): 실제 split/trim으로 구간 내부만 남기기
    #
    # 아래는 API를 지어내지 않기 위한 placeholder.
    region = None

    # 2) 질량특성 계산: MassProps로 변환
    # props = compute_mass_props(region, coordinate_system="global" or "LocalCS")
    def compute_mass_props(_region: Any) -> MassProps:
        # TODO: CHM 근거로 구현
        return MassProps(
            mass=0.0,
            cog_x=0.0,
            cog_y=0.0,
            cog_z=0.0,
            ixx=0.0,
            iyy=0.0,
            izz=0.0,
            ixy=0.0,
            iyz=0.0,
            izx=0.0,
        )

    # TODO: 형상 특징 추정(가능하면) - 근거 있는 측정 API만 사용
    def estimate_feature(_region: Any) -> Feature:
        # TODO: CHM 근거로 구현(불확실하면 unknown + estimated=True)
        return Feature(feature_type="unknown", params={}, estimated=True)

    # Segment loop
    if ranges:
        # Placeholder: user/agent must implement region extraction per range with CHM evidence.
        for idx, _r in enumerate(ranges, start=1):
            seg_region = None  # TODO: get_region_by_range(_r)
            props = compute_mass_props(seg_region)
            feature = estimate_feature(seg_region)
            write_csv_row(out_csv, segment_id=str(idx), props=props, feature=feature)
    else:
        props = compute_mass_props(region)
        feature = estimate_feature(region)
        write_csv_row(out_csv, segment_id="1", props=props, feature=feature)
    # SpaceClaim 콘솔/메시지 출력은 환경 API에 맞춰 추가


if __name__ == "__main__":
    main()
