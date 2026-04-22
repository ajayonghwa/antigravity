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
        # [단위 변환] 스페이스클레임 미터(m) 수치를 사용자용 밀리미터(mm)로 변환하는 계수
        self.display_scale = 1000.0

    def analyze_body(self, body_data):
        faces = body_data.get("faces", [])
        cylinders = [f for f in faces if f["type"] == "Cylinder"]
        conicals = [f for f in faces if f["type"] == "Conical"]
        planes = [f for f in faces if f["type"] == "Plane"]
        bends = [f for f in faces if f["type"] == "Toroidal"]
        plans = []

        if not cylinders and not conicals:
            if planes and not bends:
                plans.extend(self._generate_hgrid_plan(body_data, planes))
                return "HGRID", self._apply_beta_options(plans, body_data)
            return "COMPLEX", None

        all_curved = cylinders + conicals
        cyl_radii = [c.get("radius", 0) for c in all_curved]
        max_r = max(cyl_radii) if cyl_radii else 1.0
        threshold_radius = max_r * 0.15
        major_cyls = [c for c in all_curved if c.get("radius", 0) >= threshold_radius]
        inner_cyls = [c for c in major_cyls if c.get("is_internal", True)]
        outer_cyls = [c for c in major_cyls if not c.get("is_internal", True)]
        
        largest_cyl = max(outer_cyls, key=lambda c: c.get("radius", 0)) if outer_cyls else (max(inner_cyls, key=lambda c: c.get("radius", 0)) if inner_cyls else None)
        if not largest_cyl: return "COMPLEX", None

        main_axis = np.array(largest_cyl["axis"])
        axis_idx = np.argmax(np.abs(main_axis))

        # 1. O-grid 처리 및 간섭 회피
        parallel_major_cyls = [c for c in major_cyls if np.isclose(np.abs(np.dot(main_axis, np.array(c["axis"]))), 1.0, atol=0.01)]
        for i, feat in enumerate(parallel_major_cyls):
            plans.append(self._generate_ogrid_plan(body_data, feat, f"Core_{i}"))
            print(f" - Core O-grid added: {feat['type']}_{i} (r={feat['radius']*self.display_scale:.1f}mm)")

        # 2. 축 방향 분할 (Axial)
        all_min = np.min([f["box"]["min"][axis_idx] for f in faces])
        all_max = np.max([f["box"]["max"][axis_idx] for f in faces])
        raw_z_splits = []
        for feat in major_cyls:
            z_min, z_max = feat["box"]["min"][axis_idx], feat["box"]["max"][axis_idx]
            if not np.isclose(z_min, all_min, atol=0.001): raw_z_splits.append(z_min)
            if not np.isclose(z_max, all_max, atol=0.001): raw_z_splits.append(z_max)
        
        raw_z_splits.sort()
        merged_z = []
        if raw_z_splits:
            merged_z.append(raw_z_splits[0])
            for z in raw_z_splits[1:]:
                if z - merged_z[-1] > 0.0005: merged_z.append(z) # 0.5mm 임계값
        
        for z in merged_z:
            plans.append(self._generate_axial_split_plan(body_data, z, main_axis))
            print(f" - Axial Split at Z={z*self.display_scale:.1f}mm")

        # 3. 메타데이터에 표시용 단위 정보 주입 (Guide 전용)
        for plan in plans:
            if "core_offset" in plan:
                plan["display_offset"] = f"{plan['core_offset'] * self.display_scale:.1f}mm"
            if "split_plane" in plan:
                orig = plan["split_plane"]["origin"]
                plan["display_pos"] = f"{orig[axis_idx] * self.display_scale:.1f}mm"

        strategy_name = "AXISYMMETRIC"
        return strategy_name, self._apply_beta_options(plans, body_data)

    def _apply_beta_options(self, plans, body_data):
        for plan in plans:
            if self.options.get("mesh_recommendation"):
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
        core_offset = radius * 0.6
        
        # [지능형 회피]
        faces = body_data.get("faces", [])
        for hole in [f for f in faces if f["type"] in ["Cylinder", "Conical"] and f != cylinder_face]:
            if np.isclose(np.abs(np.dot(axis, np.array(hole["axis"]))), 1.0, atol=0.01):
                # 두 중심축 사이의 거리 계산
                dist = np.linalg.norm(np.cross(axis, np.array(hole["origin"]) - origin))
                
                # [수정] 동심원(Concentric)인 경우 간섭 회피 대상에서 제외
                if dist < 0.001: 
                    continue
                    
                h_rad = hole.get("radius", 0.0)
                # 실제로 옆에 있는 구멍과 겹칠 위험이 있을 때만 오프셋 조정
                if core_offset > dist - h_rad - 0.01:
                    new_offset = dist - h_rad - 0.01
                    core_offset = max(new_offset, radius * 0.2)
                    print(f" - Adjusted O-grid offset to {core_offset*self.display_scale:.1f}mm to avoid near hole (dist={dist*self.display_scale:.1f}mm)")

        return {
            "strategy": "OGRID",
            "body_name": body_data["body_name"],
            "hole_id": hole_id,
            "center": [float(x) for x in origin],
            "axis": [float(x) for x in axis],
            "core_offset": float(core_offset),
            "named_selections": {
                "core": f"{self.sub_device_name}_{hole_id}_OGRID_CORE",
                "outer": f"{self.sub_device_name}_{hole_id}_OGRID_OUTER"
            }
        }

    def _generate_axial_split_plan(self, body_data, coord, main_axis=[0, 0, 1]):
        origin = [0.0, 0.0, 0.0]
        axis_idx = np.argmax(np.abs(np.array(main_axis)))
        origin[axis_idx] = float(coord)
        return {
            "strategy": "AXIAL",
            "body_name": body_data["body_name"],
            "split_plane": {"origin": origin, "normal": [int(x) for x in main_axis]},
            "named_selections": {"part_a": f"{self.sub_device_name}_AXIAL_A", "part_b": f"{self.sub_device_name}_AXIAL_B"}
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
