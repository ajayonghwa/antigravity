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

        # 바디 전체 크기 계산 (외곽 구멍 판별용)
        b_min_all = np.min([f["box"]["min"] for f in faces], axis=0)
        b_max_all = np.max([f["box"]["max"] for f in faces], axis=0)
        body_center = (b_min_all + b_max_all) / 2.0
        # 메인 축 방향 결정
        all_curved = cylinders + conicals
        if all_curved:
            largest_cyl = max(all_curved, key=lambda c: c.get("radius", 0))
            main_axis = np.array(largest_cyl["axis"])
        else:
            largest_cyl = None
            main_axis = np.array([0, 0, 1])
        
        axis_idx = np.argmax(np.abs(main_axis))
        # 전체 바디의 "반경" 추정 (메인 축 수직 방향)
        v_idx = (axis_idx + 1) % 3
        body_radius = (b_max_all[v_idx] - b_min_all[v_idx]) / 2.0

        if not cylinders and not conicals:
            if planes:
                plans.extend(self._generate_hgrid_plan(body_data, planes))
                return "HGRID", self._apply_beta_options(plans, body_data)
            return "COMPLEX", None

        # 2. O-grid 계획 (중복 제거 + 외곽 필터링)
        unique_axes = []
        for feat in all_curved:
            feat_axis = np.array(feat["axis"])
            feat_origin = (np.array(feat["box"]["min"]) + np.array(feat["box"]["max"])) / 2.0
            
            # [강화된 외곽 필터링] 전체 바디 반경의 75% 이상이면 제외
            dist_from_main = np.linalg.norm(np.cross(main_axis, feat_origin - body_center))
            if dist_from_main > body_radius * 0.75:
                continue

            is_duplicate = False
            for u_feat in unique_axes:
                u_axis = np.array(u_feat["axis"])
                u_origin = (np.array(u_feat["box"]["min"]) + np.array(u_feat["box"]["max"])) / 2.0
                dist = np.linalg.norm(np.cross(u_axis, feat_origin - u_origin))
                if np.abs(np.dot(u_axis, feat_axis)) > 0.99 and dist < 0.001:
                    is_duplicate = True
                    if feat["radius"] > u_feat["radius"]: u_feat["radius"] = feat["radius"]
                    break
            if not is_duplicate: unique_axes.append(feat)

        for i, feat in enumerate(unique_axes):
            plan = self._generate_ogrid_plan(body_data, feat, f"Core_{i}")
            if plan:
                plans.append(plan)
                print(f" - Core O-grid: Offset={plan['core_offset']*self.display_scale:.1f}mm")

        # 3. 90도 섹터 분할 (전용 계획 함수 사용)
        if largest_cyl and largest_cyl["radius"] > 0.005:
            origin = (np.array(largest_cyl["box"]["min"]) + np.array(largest_cyl["box"]["max"])) / 2.0
            v1 = np.array([0.0, 0.0, 0.0])
            v1[(axis_idx + 1) % 3] = 1.0
            v1 = v1 - np.dot(v1, main_axis) * main_axis
            v1 /= np.linalg.norm(v1)
            v2 = np.cross(main_axis, v1)
            
            plans.append(self._generate_sector_split_plan(body_data, origin, v1, "Sector_A"))
            plans.append(self._generate_sector_split_plan(body_data, origin, v2, "Sector_B"))
            print(" - 90-deg Sector cross-splits planned.")

        # 4. 축 방향 단차 분할
        all_z = []
        for feat in all_curved:
            all_z.append(feat["box"]["min"][axis_idx])
            all_z.append(feat["box"]["max"][axis_idx])
        all_z.sort()
        merged_z = []
        if all_z:
            merged_z.append(all_z[0])
            for z in all_z[1:]:
                if z - merged_z[-1] > 0.002: merged_z.append(z)
        
        for z in merged_z:
            if z > b_min_all[axis_idx] + 0.001 and z < b_max_all[axis_idx] - 0.001:
                plans.append(self._generate_axial_split_plan(body_data, z, main_axis))
                print(f" - Axial Split at Z={z*self.display_scale:.1f}mm")

        return "AXISYMMETRIC", self._apply_beta_options(plans, body_data)

    def _generate_sector_split_plan(self, body_data, origin, normal, suffix):
        return {
            "strategy": "SECTOR",
            "body_name": body_data["body_name"],
            "split_plane": {"origin": [float(x) for x in origin], "normal": [float(x) for x in normal]},
            "named_selections": {"part_a": f"{self.sub_device_name}_{suffix}_A", "part_b": f"{self.sub_device_name}_{suffix}_B"}
        }

    def _generate_ogrid_plan(self, body_data, cylinder_face, hole_id):
        box = cylinder_face.get("box", {"min": [0,0,0], "max": [0,0,0]})
        origin = (np.array(box["min"]) + np.array(box["max"])) / 2.0
        axis = np.array(cylinder_face["axis"])
        radius = cylinder_face.get("radius", 1.0)
        core_offset = radius * 0.6
        
        # 간섭 회피
        faces = body_data.get("faces", [])
        for hole in [f for f in faces if "Cylinder" in f["type"] and f != cylinder_face]:
            feat_axis = np.array(hole["axis"])
            if np.isclose(np.abs(np.dot(axis, feat_axis)), 1.0, atol=0.01):
                h_box = hole.get("box", {"min": [0,0,0], "max": [0,0,0]})
                h_center = (np.array(h_box["min"]) + np.array(h_box["max"])) / 2.0
                dist = np.linalg.norm(np.cross(axis, h_center - origin))
                if dist < 0.001: continue
                h_rad = hole.get("radius", 0.0)
                if core_offset > dist - h_rad - 0.015:
                    core_offset = max(dist - h_rad - 0.015, radius * 0.15)

        return {
            "strategy": "OGRID",
            "body_name": body_data["body_name"],
            "hole_id": hole_id,
            "center": [float(x) for x in origin],
            "axis": [float(x) for x in axis],
            "core_offset": float(core_offset),
            "max_radius": float(radius),
            "named_selections": {"core": f"{self.sub_device_name}_{hole_id}_CORE", "outer": f"{self.sub_device_name}_{hole_id}_OUTER"}
        }

    def _generate_axial_split_plan(self, body_data, z_val, axis):
        origin = [0.0, 0.0, 0.0]
        idx = np.argmax(np.abs(np.array(axis)))
        origin[idx] = float(z_val)
        return {
            "strategy": "AXIAL",
            "body_name": body_data["body_name"],
            "split_plane": {"origin": origin, "normal": [float(x) for x in axis]},
            "display_pos": f"{z_val * self.display_scale:.1f}mm",
            "named_selections": {"part_a": f"{self.sub_device_name}_AXIAL_A", "part_b": f"{self.sub_device_name}_AXIAL_B"}
        }

    def _generate_hgrid_plan(self, body_data, planes):
        return [{"strategy": "HGRID", "body_name": body_data["body_name"], "split_plane": {"origin": [0,0,0], "normal": [0,0,1]}, "named_selections": {}}]

    def _apply_beta_options(self, plans, body_data):
        return plans
