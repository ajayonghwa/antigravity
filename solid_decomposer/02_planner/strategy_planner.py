import json
import numpy as np

class StrategyPlanner:
    def __init__(self, sub_device_name="DEVICE", options=None):
        self.sub_device_name = sub_device_name
        self.options = options or {
            "mesh_recommendation": True,
            "auto_merge_safety": True,
            "symmetry_check": True
        }

    def analyze_body(self, body_data):
        faces = body_data.get("faces", [])
        cylinders = [f for f in faces if f["type"] == "Cylinder"]
        planes = [f for f in faces if f["type"] == "Plane"]
        bends = [f for f in faces if f["type"] == "Toroidal"]
        plans = []

    def analyze_body(self, body_data):
        faces = body_data.get("faces", [])
        cylinders = [f for f in faces if f["type"] == "Cylinder"]
        planes = [f for f in faces if f["type"] == "Plane"]
        bends = [f for f in faces if f["type"] == "Toroidal"]
        plans = []

        if not cylinders:
            if planes and not bends:
                plans.extend(self._generate_hgrid_plan(body_data, planes))
                return "HGRID", self._apply_beta_options(plans, body_data)
            if not bends:
                return "COMPLEX", None

        # --- 유효 형상 필터링 (Major Feature Filtering) ---
        # 전체 부품 크기 대비 15% 미만의 자잘한 구멍(볼트 구멍 등)은 과감히 O-grid 대상에서 무시합니다.
        cyl_radii = [c.get("radius", 0) for c in cylinders]
        max_r = max(cyl_radii) if cyl_radii else 1.0
        threshold_radius = max_r * 0.15
        major_cyls = [c for c in cylinders if c.get("radius", 0) >= threshold_radius]
        
        # 외부 경계(Solid)와 내부 구멍(Hole) 명확히 분리
        outer_cyls = [c for c in major_cyls if not c.get("is_internal", False)]
        inner_cyls = [c for c in major_cyls if c.get("is_internal", False)]
        
        # 메인 축 결정 (가장 큰 '외부' 원통 기준, 없으면 전체 중 큰 것, 없으면 곡면 기준)
        if outer_cyls:
            largest_cyl = max(outer_cyls, key=lambda c: c.get("radius", 0))
            main_axis = np.array(largest_cyl["axis"])
        elif cylinders:
            largest_cyl = max(cylinders, key=lambda c: c.get("radius", 0))
            main_axis = np.array(largest_cyl["axis"])
        elif bends:
            # 실린더가 없고 곡면만 있는 경우
            main_axis = np.array([0, 0, 1]) # 기본값
            largest_cyl = None
        else:
            main_axis = np.array([0, 0, 1])
            largest_cyl = None

        # 1. 꺾임 관 (Bent Pipe) - 트랜스버스 컷
        cyls_with_axis = [c for c in major_cyls if "axis" in c and "origin" in c]
        if len(cyls_with_axis) >= 2:
            is_bent = False
            for c in cyls_with_axis[1:]:
                ax = np.array(c["axis"])
                if not np.isclose(np.abs(np.dot(main_axis, ax)), 1.0, atol=0.01):
                    is_bent = True
                    break
            
            if is_bent:
                unique_cuts = []
                for i, cyl in enumerate(cyls_with_axis):
                    orig = np.round(cyl["origin"], 2)
                    ax = np.round(cyl["axis"], 2)
                    cut_key = tuple(orig) + tuple(np.abs(ax))
                    if cut_key not in unique_cuts:
                        unique_cuts.append(cut_key)
                        plans.append(self._generate_transverse_split_plan(body_data, cyl, i))
                return "BENT_PIPE", self._apply_beta_options(plans, body_data)

        # 2. 토로이달 곡면 (Elbow Pipe) 처리
        if bends:
            for bend in bends:
                origin = bend.get("origin", [0,0,0])
                axis_idx = np.argmax(np.abs(main_axis))
                split_coord = origin[axis_idx]
                plans.append(self._generate_axial_split_plan(body_data, split_coord, main_axis))
            return "ELBOW_PIPE", self._apply_beta_options(plans, body_data)

        # 3. 범용 축대칭 분할 (AXISYMMETRIC)
        # 어떤 형태의 원통형 부품(다공판, 파이프, 접합부, 사각블록의 메인홀 등)이든 이 하나의 지능적인 흐름으로 완벽히 분할합니다.
        
        # 주축과 평행한 유효 원통들 (메인 몸통 + 평행한 내부 구멍)
        parallel_major_cyls = [c for c in major_cyls if np.isclose(np.abs(np.dot(main_axis, np.array(c["axis"]))), 1.0, atol=0.01)]
        
        # 3-1. 교차하는 측면 구멍 (Side holes / Junction) 파악
        # 기울어진 구멍(Y-Junction 등)이나 O-grid는 오직 '내부 구멍(inner_cyls)'에 대해서만 수행해야 합니다.
        side_holes = [c for c in inner_cyls if not np.isclose(np.abs(np.dot(main_axis, np.array(c["axis"]))), 1.0, atol=0.01)]
        for i, hole in enumerate(side_holes):
            dot_val = np.abs(np.dot(main_axis, np.array(hole["axis"])))
            if dot_val > 0.1 and dot_val < 0.9: # 기울어진 경우
                plans.append(self._generate_transverse_split_plan(body_data, hole, f"Junction_{i}"))
            else:
                plans.append(self._generate_ogrid_plan(body_data, hole, f"SideHole_{i}"))

        # 3-2. 중심축 기준 십자 분할 (Sector Split)
        if largest_cyl:
            origin = np.array(largest_cyl["origin"])
            plans.extend(self._generate_sector_split_plan(body_data, main_axis, origin))
        
        # 3-3. 축 방향 단차 및 피쳐 격리 (Axial Split)
        # 모든 주요 실린더의 시작/끝 지점을 추적하여 복합 단차 구역을 완벽히 격리합니다.
        z_splits = []
        axis_idx = np.argmax(np.abs(main_axis))
        for cyl in parallel_major_cyls:
            for val in [cyl["box"]["min"][axis_idx], cyl["box"]["max"][axis_idx]]:
                if not any(np.isclose(val, existing, atol=0.01) for existing in z_splits):
                    z_splits.append(val)
        
        z_splits.sort()
        # 보스 레벨 대응: 너무 좁은 구간이 아니면 모든 주요 지점을 분할
        for z in z_splits[1:-1]:
            plans.append(self._generate_axial_split_plan(body_data, z, main_axis))

        return "AXISYMMETRIC", self._apply_beta_options(plans, body_data)

    def _apply_beta_options(self, plans, body_data):
        """
        베타 옵션(메쉬 추천, 안전성 검사)을 계획에 적용합니다.
        """
        for plan in plans:
            # 1. 메쉬 크기 추천 (Beta)
            if self.options.get("mesh_recommendation"):
                recommended_size = 2.0 
                if "core_offset" in plan:
                    recommended_size = round(plan["core_offset"] / 3.0, 1)
                
                # NS 이름에 추천 사이즈 추가
                for key in plan["named_selections"]:
                    plan["named_selections"][key] += f"_SIZE_{recommended_size}mm"

            # 2. 자동 병합 안전성 (Beta)
            if self.options.get("auto_merge_safety"):
                if plan.get("core_offset", 10) < 0.5:
                    plan["warning"] = "Too small split detected. Consider merging."

        return plans

    def _generate_ogrid_plan(self, body_data, cylinder_face, hole_id="Core"):
        origin = cylinder_face["origin"]
        axis = cylinder_face["axis"]
        radius = cylinder_face.get("radius", 1.0)
        core_offset = radius * 0.6
        
        plan = {
            "strategy": "OGRID",
            "body_name": body_data["body_name"],
            "hole_id": hole_id,
            "center": origin,
            "axis": axis,
            "core_offset": core_offset,
            "named_selections": {
                "core": f"{self.sub_device_name}_{hole_id}_OGRID_CORE",
                "outer": f"{self.sub_device_name}_{hole_id}_OGRID_OUTER"
            }
        }
        return plan

    def _generate_hgrid_plan(self, body_data, planes):
        min_pt = np.min([f["box"]["min"] for f in planes], axis=0)
        max_pt = np.max([f["box"]["max"] for f in planes], axis=0)
        size = max_pt - min_pt
        long_axis_idx = np.argmax(size)
        split_coord = (min_pt[long_axis_idx] + max_pt[long_axis_idx]) / 2.0
        origin = [(min_pt[i] + max_pt[i]) / 2.0 for i in range(3)]
        origin[long_axis_idx] = split_coord
        normal = [0, 0, 0]
        normal[long_axis_idx] = 1
        
        plan = {
            "strategy": "HGRID",
            "body_name": body_data["body_name"],
            "split_plane": {
                "origin": [float(x) for x in origin],
                "normal": [int(x) for x in normal]
            },
            "named_selections": {
                "part_a": f"{self.sub_device_name}_HGRID_A",
                "part_b": f"{self.sub_device_name}_HGRID_B"
            }
        }
        return [plan]

    def _generate_axial_split_plan(self, body_data, coord, main_axis=[0, 0, 1]):
        axis_arr = np.array(main_axis)
        origin = [0.0, 0.0, 0.0]
        axis_idx = np.argmax(np.abs(axis_arr))
        origin[axis_idx] = float(coord)
        
        plan = {
            "strategy": "AXIAL",
            "body_name": body_data["body_name"],
            "split_plane": {
                "origin": origin,
                "normal": [float(x) for x in main_axis]
            },
            "named_selections": {
                "part_upper": f"{self.sub_device_name}_AXIAL_{coord}_UP",
                "part_lower": f"{self.sub_device_name}_AXIAL_{coord}_LOW"
            }
        }
        return plan

    def _generate_transverse_split_plan(self, body_data, cylinder, idx):
        axis = cylinder["axis"]
        origin = cylinder["origin"]
        
        plan = {
            "strategy": "TRANSVERSE",
            "body_name": body_data["body_name"],
            "split_plane": {
                "origin": [float(x) for x in origin],
                "normal": [float(x) for x in axis]
            },
            "named_selections": {
                "part_a": f"{self.sub_device_name}_BENT_{idx}_A",
                "part_b": f"{self.sub_device_name}_BENT_{idx}_B"
            }
        }
        return plan

    def _generate_sector_split_plan(self, body_data, main_axis, origin):
        # 십자 분할(90도 간격)을 위해 주축(main_axis)에 수직인 두 개의 직교 벡터 계산
        axis = np.array(main_axis)
        v1 = np.array([1.0, 0.0, 0.0])
        if np.isclose(np.abs(np.dot(axis, v1)), 1.0):
            v1 = np.array([0.0, 1.0, 0.0])
            
        n1 = v1 - np.dot(v1, axis) * axis
        n1 = n1 / np.linalg.norm(n1)
        
        n2 = np.cross(axis, n1)
        n2 = n2 / np.linalg.norm(n2)
        
        origin1 = np.array(origin)
        # 십자 교차점 위상 에러 회피를 위해 두 번째 절단면을 0.01mm 미세 이동
        origin2 = origin1 + n1 * 0.01
        
        plans = []
        plans.append({
            "strategy": "SECTOR",
            "body_name": body_data["body_name"],
            "split_plane": {
                "origin": [float(x) for x in origin1],
                "normal": [float(x) for x in n1]
            },
            "named_selections": {"part_a": f"{self.sub_device_name}_SEC1_A", "part_b": f"{self.sub_device_name}_SEC1_B"}
        })
        plans.append({
            "strategy": "SECTOR",
            "body_name": body_data["body_name"],
            "split_plane": {
                "origin": [float(x) for x in origin2],
                "normal": [float(x) for x in n2]
            },
            "named_selections": {"part_a": f"{self.sub_device_name}_SEC2_A", "part_b": f"{self.sub_device_name}_SEC2_B"}
        })
        return plans

    def get_ai_advice(self, body_data):
        return "해당 형상은 분기점이 복잡합니다. 메인 바디와 연결된 파이프의 접합부를 기준으로 평면 분할을 먼저 시도하세요."
