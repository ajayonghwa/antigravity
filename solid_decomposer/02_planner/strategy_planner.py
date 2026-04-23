import json
import numpy as np
import math

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

class StrategyPlanner:
    def __init__(self, sub_device_name="DEVICE", options=None):
        self.sub_device_name = sub_device_name
        self.options = options or {
            "mesh_recommendation": True,
            "auto_merge_safety": True,
            "symmetry_check": True
        }
        self.display_scale = 1000.0

    def analyze_body(self, body_data, units="m"):
        self.units = units
        faces = body_data.get("faces", [])
        self.body_data = body_data
        
        self.cylinders = [f for f in faces if "Cylinder" in f["type"]]
        self.conicals = [f for f in faces if "Conical" in f["type"]]
        self.planes = [f for f in faces if "Plane" in f["type"]]
        self.toroidals = [f for f in faces if "Toroidal" in f["type"]]
        self.all_curved = self.cylinders + self.conicals
        
        if not faces:
            return "UNKNOWN", []

        # 바디 전체 크기 계산
        b_min_all = np.min([f["box"]["min"] for f in faces], axis=0)
        b_max_all = np.max([f["box"]["max"] for f in faces], axis=0)
        self.body_center = (b_min_all + b_max_all) / 2.0
        self.body_size = b_max_all - b_min_all
        self.body_volume = body_data.get("volume", 0)

        # 1. 형상 분류 (Classification)
        classification = self._classify_body()
        
        # 2. 전략 생성
        plans = []
        if classification == "FASTENER":
            plans.extend(self._plan_fastener())
        elif classification == "ELBOW":
            plans.extend(self._plan_elbow())
        elif classification == "THIN_WALL_CYLINDER":
            plans.extend(self._plan_thin_wall())
        elif classification == "PERFORATED_PLATE":
            plans.extend(self._plan_perforated())
        elif classification == "CROSS_HOLE":
            plans.extend(self._plan_cross_hole())
        elif classification == "PROTRUDING_BOSS":
            plans.extend(self._plan_boss())
        elif classification == "PIPE_JUNCTION":
            plans.extend(self._plan_junction())
        elif classification == "THICK_WALL_CYLINDER":
            plans.extend(self._plan_thick_wall())
        elif classification == "PRISMATIC":
            plans.extend(self._plan_prismatic())
        else:
            print(f" - Body classified as {classification}. Using fallback strategy.")
        
        return classification, self._apply_beta_options(plans, body_data)

    def _classify_body(self):
        """7대 실무 형상 맞춤형 분류기"""
        # 1. Fastener (볼트/와셔) - 전체 모델 대비 너무 작은 경우 (여기서는 절대 볼륨으로 임시 처리)
        if self.body_volume > 0 and self.body_volume < 1e-6: # 1cm^3 미만
            if self.all_curved:
                return "FASTENER"
                
        # 2. Elbow (휘어진 관)
        if self.toroidals:
            return "ELBOW"
            
        if not self.all_curved:
            if self.planes: return "PRISMATIC"
            return "COMPLEX"
            
        # 축별 그룹화
        axis_groups = self._group_by_axis(self.all_curved)
        
        # 3. 다중 축 교차
        if len(axis_groups) >= 2:
            main_g = axis_groups[0]
            sub_g = axis_groups[1]
            angle = abs(np.dot(main_g["axis"], sub_g["axis"]))
            
            # 파이프 교차 (Y-Block) - 각도가 70도 이상 교차 (cos 70도 ~ 0.34)
            if angle < 0.34: 
                # 면적이 평면이 지배적이고 구멍이 많으면 다공판, 아니면 교차 파이프/크로스홀
                plane_area = sum([f.get("area", 0) for f in self.planes])
                cyl_area = sum([f.get("area", 0) for f in self.all_curved])
                
                if plane_area > cyl_area * 2 and len(main_g["holes"]) > 3:
                    return "PERFORATED_PLATE"
                else:
                    # 메인 그룹과 서브 그룹이 직교에 가까우면 Cross Hole
                    if angle < 0.1:
                        return "CROSS_HOLE"
                    return "PIPE_JUNCTION"

        # 4. 단일 축 (Thin Wall, Thick Wall, Boss, Axisymmetric)
        if len(axis_groups) == 1:
            g = axis_groups[0]
            radii = [h.get("radius", 0) for h in g["holes"] if h.get("radius", 0) > 0]
            
            # 돌출 블록 판별 (실린더 외곽을 벗어나는 평면 존재)
            # 여기서는 단순화를 위해 Bounding Box 극단에 평면이 있는지 확인
            is_boss = False
            for p in self.planes:
                if p.get("area", 0) > np.max(self.body_size)**2 * 0.1:
                    is_boss = True # 단순화된 조건
            
            if is_boss and len(self.planes) > len(self.all_curved):
                return "PROTRUDING_BOSS"

            # 다공판(Perforated Plate) 우선 판별 (구멍이 3개 이상이면 파이프가 아님)
            plane_area = sum([f.get("area", 0) for f in self.planes])
            cyl_area = sum([f.get("area", 0) for f in self.all_curved])
            if (plane_area > cyl_area * 1.5 or len(g["holes"]) > 2):
                 return "PERFORATED_PLATE"

            # 단일 축 파이프/보스 판별
            if len(radii) >= 2:
                r_max = max(radii)
                r_min = min(radii)
                if r_min > 0.001:
                    ratio = r_max / r_min
                    if ratio < 1.05: # 외경/내경 차이가 5% 미만
                        return "THIN_WALL_CYLINDER"
                    elif ratio > 1.2:
                        return "THICK_WALL_CYLINDER" 

        return "AXISYMMETRIC"

    def _group_by_axis(self, curved_faces):
        groups = []
        for feat in curved_faces:
            if "axis" not in feat: continue
            feat_axis = normalize(np.array(feat["axis"]))
            matched = False
            for g in groups:
                if abs(np.dot(g["axis"], feat_axis)) > 0.95:
                    g["holes"].append(feat)
                    matched = True
                    break
            if not matched:
                groups.append({"axis": feat_axis, "holes": [feat]})
        
        # 구멍 면적 합계로 정렬 (주축 결정)
        groups.sort(key=lambda g: sum([h.get("area", 0) for h in g["holes"]]), reverse=True)
        return groups

    # --- Strategy Implementations ---

    def _plan_fastener(self):
        print(" - Fastener detected. Skipping complex decomp.")
        # 단순 Sector 분할만 적용 (주축 기준)
        if not self.all_curved: return []
        main_axis = normalize(np.array(self.all_curved[0].get("axis", [0,0,1])))
        return self._generate_cross_sectors(self.body_center, main_axis)

    def _plan_elbow(self):
        print(" - Elbow pipe detected.")
        plans = []
        for t in self.toroidals:
            if "origin" in t and "axis" in t: # Assuming toroidals have axis
                # 횡단면 분할 (Sweep Path Cut)
                pass # 구체적 로직은 향후 구현
        return plans

    def _plan_thin_wall(self):
        print(" - Thin-walled cylinder. Skipping O-Grid.")
        groups = self._group_by_axis(self.all_curved)
        main_axis = groups[0]["axis"]
        return self._generate_cross_sectors(self.body_center, main_axis)

    def _plan_thick_wall(self):
        print(" - Thick-walled cylinder detected. Applying O-Grid + Sectors.")
        plans = []
        groups = self._group_by_axis(self.all_curved)
        main_axis = groups[0]["axis"]
        # 1. Sector
        plans.extend(self._generate_cross_sectors(self.body_center, main_axis))
        # 2. O-Grid for inner holes
        for h in groups[0]["holes"]:
            plans.extend(self._plan_ogrid_for_hole(h, main_axis))
        return plans

    def _plan_perforated(self):
        print(" - Perforated plate detected. Analyzing interference for {0} holes.".format(len(self.all_curved)))
        plans = []
        groups = self._group_by_axis(self.all_curved)
        if not groups: return []
        main_axis = groups[0]["axis"]
        holes = groups[0]["holes"]
        
        # 1. 구멍 크기순 정렬 (큰 것 우선)
        holes.sort(key=lambda h: h.get("radius", 0), reverse=True)
        
        # [v4.7] 3. 간섭을 고려한 O-Grid 계획
        for i, h1 in enumerate(holes):
            o1 = np.array(h1.get("origin", [0,0,0]))
            r1 = h1.get("radius", 0)
            min_gap = 1e9
            
            for j, h2 in enumerate(holes):
                if i == j: continue
                o2 = np.array(h2.get("origin", [0,0,0]))
                dist = np.linalg.norm(o1 - o2)
                gap = dist - (r1 + h2.get("radius", 0))
                if gap < min_gap: min_gap = gap
            
            # [v4.7] 첫 번째(가장 큰) 구멍은 안전 장치를 더 느슨하게 적용
            is_main = (i == 0)
            plans.extend(self._plan_ogrid_for_hole(h1, main_axis, neighbor_gap=min_gap, is_main=is_main))
            
        # [v4.4 추가] 원판 전체에 대한 4분할(Sector) - 가장 큰 구멍(또는 바디 센터) 기준
        if len(holes) > 0:
            # 가장 큰 구멍의 중심을 찾음
            main_hole = holes[0] # 이미 크기순 정렬됨
            h_box = main_hole.get("box", {"min": [0,0,0], "max": [0,0,0]})
            h_center = (np.array(h_box["min"]) + np.array(h_box["max"])) / 2.0
            plans.extend(self._generate_cross_sectors(h_center, main_axis))
            
        return plans

    def _plan_cross_hole(self):
        print(" - Cross-drilled cylinder detected.")
        plans = []
        groups = self._group_by_axis(self.all_curved)
        main_axis = groups[0]["axis"]
        sub_axis = groups[1]["axis"]
        
        # Sector 분할 시 서브 축(구멍)을 피하도록 각도 조정 (45도)
        v1 = np.cross(main_axis, sub_axis)
        v1 = normalize(v1)
        # 45도 회전
        cos45 = math.cos(math.pi/4)
        sin45 = math.sin(math.pi/4)
        v_rot = v1 * cos45 + np.cross(main_axis, v1) * sin45 + main_axis * np.dot(main_axis, v1) * (1-cos45)
        
        plans.append(self._generate_sector_split_plan(self.body_center, v_rot, "Sector_Avoid_A"))
        plans.append(self._generate_sector_split_plan(self.body_center, np.cross(main_axis, v_rot), "Sector_Avoid_B"))
        
        # O-Grids
        for h in groups[0]["holes"]: plans.extend(self._plan_ogrid_for_hole(h, main_axis))
        for h in groups[1]["holes"]: plans.extend(self._plan_ogrid_for_hole(h, sub_axis))
        return plans

    def _plan_boss(self):
        print(" - Protruding boss detected.")
        groups = self._group_by_axis(self.all_curved)
        main_axis = groups[0]["axis"] if groups else np.array([0,0,1])
        plans = self._generate_cross_sectors(self.body_center, main_axis)
        for h in self.all_curved: plans.extend(self._plan_ogrid_for_hole(h, normalize(np.array(h.get("axis", [0,0,1])))))
        return plans

    def _plan_junction(self):
        print(" - Pipe junction detected. Applying Y-Block.")
        plans = []
        groups = self._group_by_axis(self.all_curved)
        a1 = groups[0]["axis"]
        a2 = groups[1]["axis"]
        
        bisector = normalize(a1 + a2)
        perp = normalize(np.cross(a1, a2))
        
        plans.append({"strategy": "YBLOCK_CUT", "body_name": self.body_data["body_name"], "split_plane": {"origin": self.body_center.tolist(), "normal": bisector.tolist()}})
        plans.append({"strategy": "YBLOCK_CUT", "body_name": self.body_data["body_name"], "split_plane": {"origin": self.body_center.tolist(), "normal": perp.tolist()}})
        return plans

    def _plan_axisymmetric(self):
        plans = []
        groups = self._group_by_axis(self.all_curved)
        main_axis = groups[0]["axis"]
        
        # 1. Sector
        plans.extend(self._generate_cross_sectors(self.body_center, main_axis))
        
        # 2. Axial Optimization
        axis_idx = np.argmax(np.abs(main_axis))
        z_radius_map = {}
        for feat in self.all_curved:
            z_min = feat["box"]["min"][axis_idx]
            z_max = feat["box"]["max"][axis_idx]
            r = feat.get("radius", 0)
            for z in [z_min, z_max]:
                z_key = round(z, 4)
                if z_key not in z_radius_map: z_radius_map[z_key] = set()
                z_radius_map[z_key].add(round(r, 5))
                
        for z, radii in sorted(z_radius_map.items()):
            if len(radii) >= 2: # 직경 변화 구간
                 # 바운딩 박스 끝단은 제외
                 if z > self.body_center[axis_idx] - self.body_size[axis_idx]/2 + 0.002 and z < self.body_center[axis_idx] + self.body_size[axis_idx]/2 - 0.002:
                     origin = [0,0,0]
                     origin[axis_idx] = float(z)
                     plans.append({
                         "strategy": "AXIAL",
                         "body_name": self.body_data["body_name"],
                         "split_plane": {"origin": origin, "normal": main_axis.tolist()},
                         "display_pos": f"{z * self.display_scale:.1f}mm"
                     })
                     print(f" - Optimized Axial Split at Z={z*self.display_scale:.1f}mm")

        # 3. O-Grid (WHR 기반)
        for h in self.all_curved:
             plans.extend(self._plan_ogrid_for_hole(h, normalize(np.array(h.get("axis", main_axis)))))
             
        return plans

    def _plan_prismatic(self):
        plans = []
        longest_axis = np.argmax(self.body_size)
        normal = [0, 0, 0]
        normal[longest_axis] = 1.0
        plans.append({
            "strategy": "HGRID",
            "body_name": self.body_data["body_name"],
            "split_plane": {"origin": self.body_center.tolist(), "normal": normal},
        })
        return plans

    # --- Utility Functions ---

    def _generate_cross_sectors(self, origin, main_axis):
        axis_idx = np.argmax(np.abs(main_axis))
        v1 = np.array([0.0, 0.0, 0.0])
        v1[(axis_idx + 1) % 3] = 1.0
        v1 = normalize(v1 - np.dot(v1, main_axis) * main_axis)
        v2 = np.cross(main_axis, v1)
        return [
            self._generate_sector_split_plan(origin, v1, "Sector_A"),
            self._generate_sector_split_plan(origin, v2, "Sector_B")
        ]

    def _generate_sector_split_plan(self, origin, normal, suffix):
        return {
            "strategy": "SECTOR",
            "body_name": self.body_data["body_name"],
            "split_plane": {"origin": [float(x) for x in origin], "normal": [float(x) for x in normal]}
        }

    def _plan_ogrid_for_hole(self, hole, axis, neighbor_gap=None, is_main=False):
        radius = hole.get("radius", 0)
        # [v4.56] 단위(units)에 따른 임계값 조정 (m: 0.0001, mm: 0.1)
        is_mm = (self.units == "mm")
        threshold = 0.1 if is_mm else 0.0001
        
        if radius < threshold: 
            print("    [SKIP] Radius too small: {0:.4f}{1}".format(radius, self.units))
            return [] 
        
        is_internal = hole.get("is_internal", True)
        if is_internal:
            safe_offset = radius * 1.3
            if neighbor_gap is not None and neighbor_gap < (safe_offset - radius) * 2:
                safe_offset = radius + (neighbor_gap * 0.4)
        else:
            safe_offset = radius * 0.7
            
        origin = np.array(hole.get("origin", self.body_center))
        min_wall_dist = float('inf')
        # 바디 경계면과의 거리 계산 (전역 좌표계 기준)
        for i in range(3):
            if abs(axis[i]) < 0.5:
                # [v4.80] 바디 센터와 사이즈를 이용한 벽면 거리 계산
                d1 = abs(origin[i] - (self.body_center[i] - self.body_size[i]/2))
                d2 = abs(origin[i] - (self.body_center[i] + self.body_size[i]/2))
                min_wall_dist = min(min_wall_dist, d1, d2)
        
        rib_thickness = min_wall_dist - radius
        
        # [v4.7] 메인 구멍은 웬만하면 스킵하지 않음
        safety_limit = radius * 0.1 if not is_main else (0.1 if is_mm else 0.0001)
        
        # 로그 출력용 스케일 (이미 mm면 1배, m면 1000배)
        log_scale = 1.0 if is_mm else 1000.0
        
        if rib_thickness < safety_limit:
            print("    [SKIP] Rib too thin: {0:.2f}mm (Limit: {1:.2f}mm) for Hole at {2}".format(
                rib_thickness * log_scale, safety_limit * log_scale, [round(x * log_scale, 1) for x in origin]))
            return []
            
        print("    [PLAN] O-Grid for hole at {0}: Offset={1:.2f}mm".format(
            [round(x * log_scale, 1) for x in origin], safe_offset * log_scale))
        return [self._create_ogrid_dict(hole, axis, safe_offset)]

    def _create_ogrid_dict(self, hole, axis, offset):
        # [v4.4] 가장 안정적인 바운딩 박스 중앙값 사용 (Stable v1 방식)
        box = hole.get("box", {"min": [0,0,0], "max": [0,0,0]})
        origin = (np.array(box["min"]) + np.array(box["max"])) / 2.0
            
        return {
            "strategy": "OGRID",
            "body_name": self.body_data["body_name"],
            "center": [float(x) for x in origin],
            "axis": [float(x) for x in axis],
            "core_offset": float(offset),
            "max_radius": float(hole.get("radius", 0))
        }

    def _apply_beta_options(self, plans, body_data):
        return plans
