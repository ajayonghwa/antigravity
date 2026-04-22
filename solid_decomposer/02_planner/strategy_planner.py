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
        self.display_scale = 1000.0

    def analyze_body(self, body_data):
        faces = body_data.get("faces", [])
        cylinders = [f for f in faces if "Cylinder" in f["type"]]
        conicals = [f for f in faces if "Conical" in f["type"]]
        planes = [f for f in faces if "Plane" in f["type"]]
        plans = []

        if not cylinders and not conicals:
            if planes:
                plans.extend(self._generate_hgrid_plan(body_data, planes))
                return "HGRID", self._apply_beta_options(plans, body_data)
            return "COMPLEX", None

        # 1. 메인 축 결정 (가장 큰 원통 기준)
        all_curved = cylinders + conicals
        largest_cyl = max(all_curved, key=lambda c: c.get("radius", 0))
        main_axis = np.array(largest_cyl["axis"])
        axis_idx = np.argmax(np.abs(main_axis))

        # 2. 중복 제거된 O-grid 계획 수립 (축이 같으면 하나만)
        # 축 방향이 같고 위치가 거의 같은 실린더들을 그룹화합니다.
        unique_axes = []
        for feat in all_curved:
            feat_axis = np.array(feat["axis"])
            feat_origin = np.array(feat["origin"])
            
            is_duplicate = False
            for u_feat in unique_axes:
                u_axis = np.array(u_feat["axis"])
                u_origin = np.array(u_feat["origin"])
                
                # 축이 평행하고 중심선 거리가 매우 가까우면 동심원으로 판단
                dist = np.linalg.norm(np.cross(u_axis, feat_origin - u_origin))
                axis_dot = np.abs(np.dot(u_axis, feat_axis))
                if axis_dot > 0.99 and dist < 0.001:
                    is_duplicate = True
                    # 더 큰 반경을 가진 것을 대표로 유지
                    if feat["radius"] > u_feat["radius"]:
                        u_feat["radius"] = feat["radius"]
                    break
            
            if not is_duplicate:
                unique_axes.append(feat)

        # O-grid 추가
        for i, feat in enumerate(unique_axes):
            plan = self._generate_ogrid_plan(body_data, feat, f"Core_{i}")
            plans.append(plan)
            # [수치 통일] 반경이 아닌 '코어 오프셋' 수치를 출력하여 혼란 방지
            print(f" - Core O-grid added: {feat['type']} (Offset={plan['core_offset']*self.display_scale:.1f}mm)")

        # 3. 90도 섹터 분할 (Sector Split)
        # 메인 원통이 있고 충분히 크다면 십자 분할을 추가합니다.
        if largest_cyl and largest_cyl["radius"] > 0.005:
            origin = np.array(largest_cyl["origin"])
            v1 = np.array([0, 0, 0], dtype=float)
            v1[(axis_idx + 1) % 3] = 1.0
            v1 = v1 - np.dot(v1, main_axis) * main_axis
            v1 /= np.linalg.norm(v1)
            v2 = np.cross(main_axis, v1)
            
            plans.append(self._generate_axial_split_plan(body_data, origin, v1, "Sector_A"))
            plans.append(self._generate_axial_split_plan(body_data, origin, v2, "Sector_B"))
            print(" - 90-deg Sector cross-splits planned.")

        # 4. 축 방향 단차 분할 (Axial)
        all_z = []
        for feat in all_curved:
            all_z.append(feat["box"]["min"][axis_idx])
            all_z.append(feat["box"]["max"][axis_idx])
        
        all_z.sort()
        # [강화] 병합 임계값을 2mm로 늘려 아주 인접한 단차는 하나로 처리
        merged_z = []
        if all_z:
            merged_z.append(all_z[0])
            for z in all_z[1:]:
                if z - merged_z[-1] > 0.002: merged_z.append(z)
        
        # [강화] 경계면 제외 로직 (0.5mm 여유를 두어 Z=0 등 제외)
        b_min = np.min([f["box"]["min"][axis_idx] for f in faces])
        b_max = np.max([f["box"]["max"][axis_idx] for f in faces])
        
        for z in merged_z:
            if z > b_min + 0.0005 and z < b_max - 0.0005:
                plans.append(self._generate_axial_split_plan(body_data, z, main_axis))
                print(f" - Axial Split at Z={z*self.display_scale:.1f}mm")

        # 메타데이터 주입
        for plan in plans:
            if "core_offset" in plan:
                plan["display_offset"] = f"{plan['core_offset'] * self.display_scale:.1f}mm"
            if "split_plane" in plan:
                orig = plan["split_plane"]["origin"]
                plan["display_pos"] = f"{orig[axis_idx] * self.display_scale:.1f}mm"

        return "AXISYMMETRIC", self._apply_beta_options(plans, body_data)

    def _apply_beta_options(self, plans, body_data):
        for plan in plans:
            recommended_size = 2.0 
            if "core_offset" in plan:
                recommended_size = round((plan["core_offset"] * self.display_scale) / 3.0, 1)
            for key in plan["named_selections"]:
                plan["named_selections"][key] += f"_SIZE_{recommended_size}mm"
        return plans

    def _generate_ogrid_plan(self, body_data, cylinder_face, hole_id="Core"):
        origin = np.array(cylinder_face["origin"])
        axis = np.array(cylinder_face["axis"])
        radius = cylinder_face.get("radius", 1.0)
        # 초기 코어 오프셋은 반경의 60%
        core_offset = radius * 0.6
        
        # [강화된 지능형 회피]
        faces = body_data.get("faces", [])
        for hole in [f for f in faces if "Cylinder" in f["type"] and f != cylinder_face]:
            feat_axis = np.array(hole["axis"])
            if np.isclose(np.abs(np.dot(axis, feat_axis)), 1.0, atol=0.01):
                dist = np.linalg.norm(np.cross(axis, np.array(hole["origin"]) - origin))
                if dist < 0.001: continue # 동심원은 이미 처리됨
                
                h_rad = hole.get("radius", 0.0)
                # 커터들끼리 겹치지 않도록 마진을 15mm(0.015m)로 확대
                safe_limit = dist - h_rad - 0.015
                if core_offset > safe_limit:
                    core_offset = max(safe_limit, radius * 0.15)
                    print(f" - Tight space detected! Reducing O-grid offset to {core_offset*self.display_scale:.1f}mm to avoid near hole.")

        return {
            "strategy": "OGRID",
            "body_name": body_data["body_name"],
            "hole_id": hole_id,
            "center": [float(x) for x in origin],
            "axis": [float(x) for x in axis],
            "core_offset": float(core_offset),
            "max_radius": float(radius), # 커터 크기 결정용
            "named_selections": {
                "core": f"{self.sub_device_name}_{hole_id}_OGRID_CORE",
                "outer": f"{self.sub_device_name}_{hole_id}_OGRID_OUTER"
            }
        }

    def _generate_axial_split_plan(self, body_data, z_or_origin, axis, suffix="AXIAL"):
        if isinstance(z_or_origin, (float, int)):
            origin = [0.0, 0.0, 0.0]
            axis_idx = np.argmax(np.abs(np.array(axis)))
            origin[axis_idx] = float(z_or_origin)
        else:
            origin = [float(x) for x in z_or_origin]
            
        return {
            "strategy": "AXIAL",
            "body_name": body_data["body_name"],
            "split_plane": {"origin": origin, "normal": [float(x) for x in axis]},
            "named_selections": {"part_a": f"{self.sub_device_name}_{suffix}_A", "part_b": f"{self.sub_device_name}_{suffix}_B"}
        }

    def _generate_hgrid_plan(self, body_data, planes):
        min_pt = np.min([f["box"]["min"] for f in planes], axis=0)
        max_pt = np.max([f["box"]["max"] for f in planes], axis=0)
        center = (min_pt + max_pt) / 2.0
        return [{
            "strategy": "HGRID",
            "body_name": body_data["body_name"],
            "split_plane": {"origin": [float(x) for x in center], "normal": [0, 0, 1]},
            "named_selections": {"part_a": f"{self.sub_device_name}_HGRID_A", "part_b": f"{self.sub_device_name}_HGRID_B"}
        }]
