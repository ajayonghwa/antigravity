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
        conicals = [f for f in faces if f["type"] == "Conical"] # 테이퍼 추가
        planes = [f for f in faces if f["type"] == "Plane"]
        bends = [f for f in faces if f["type"] == "Toroidal"]
        plans = []

        if not cylinders and not conicals:
            if planes and not bends:
                plans.extend(self._generate_hgrid_plan(body_data, planes))
                return "HGRID", self._apply_beta_options(plans, body_data)
            if not bends:
                return "COMPLEX", None

        # --- 유효 형상 필터링 (Major Feature Filtering) ---
        all_curved = cylinders + conicals
        cyl_radii = [c.get("radius", 0) for c in all_curved]
        max_r = max(cyl_radii) if cyl_radii else 1.0
        threshold_radius = max_r * 0.15
        major_cyls = [c for c in all_curved if c.get("radius", 0) >= threshold_radius]
        
        # 외부 돌출부(Boss)와 내부 구멍(Hole) 분류
        inner_cyls = [c for c in major_cyls if c.get("is_internal", True)]
        outer_cyls = [c for c in major_cyls if not c.get("is_internal", True)]
        
        # [지능형 판단] 주축 결정 시 외부 원통(Boss/Shell)을 우선하되 구멍도 고려
        largest_cyl = None
        if outer_cyls:
            largest_cyl = max(outer_cyls, key=lambda c: c.get("radius", 0))
        elif inner_cyls:
            largest_cyl = max(inner_cyls, key=lambda c: c.get("radius", 0))

        if not largest_cyl:
            return "COMPLEX", None

        main_axis = np.array(largest_cyl["axis"])

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
                        # [시니어 지능] 교차로 코어 블록화 전략
                        # 단일 컷 대신, 교차점 주변을 파이프 반경만큼 앞뒤로 잘라 코어를 가둡니다.
                        radius = cyl.get("radius", 20.0)
                        axis = np.array(cyl["axis"])
                        pos = np.array(cyl["origin"])
                        
                        # 교차점 기준 앞뒤로 분할 (Core Isolation)
                        plans.append(self._generate_axial_split_plan(body_data, np.dot(pos + axis*radius, axis), axis))
                        plans.append(self._generate_axial_split_plan(body_data, np.dot(pos - axis*radius, axis), axis))
                        print(f" - Junction Core Isolation added for Pipe_{i}")
                
                return "JUNCTION_CORE", self._apply_beta_options(plans, body_data)

        # 2. 토로이달 곡면 (Elbow Pipe) 처리
        # [지능형 필터] 반지름이 너무 작은 토로이달 면은 엘보우가 아니라 '필렛(Fillet)'입니다.
        major_bends = [b for b in bends if b.get("radius", 0) > 10.0] # 10mm 이상만 엘보우로 인정
        if major_bends:
            plans.append(self._generate_elbow_split_plan(body_data, major_bends[0]))
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

        # [지능형 판단] 몸체 특성 파악 (박스 기반, 다공판, 비대칭 피쳐 여부)
        is_block_based = len(planes) > len(cylinders) + 2
        is_perforated = len(inner_cyls) >= 4 
        
        # [핵심] 비대칭 피쳐 감지: 90도 각도에 정렬되지 않은 평면이 있으면 '비대칭'으로 간주
        has_asymmetric_feature = False
        for p in planes:
            norm = np.abs(np.array(p.get("normal", [0,0,1])))
            # X, Y, Z 축과 정렬되지 않은 평면이 있는지 확인 (0, 1 외의 값)
            if not any(np.isclose(norm, [1,0,0], atol=0.01)) and \
               not any(np.isclose(norm, [0,1,0], atol=0.01)) and \
               not any(np.isclose(norm, [0,0,1], atol=0.01)):
                has_asymmetric_feature = True
                break

        # 3-3. 메인 축방향 O-grid 처리 (최우선 순위)
        # 이제 모든 주요 원기둥(Hole & Solid Body)에 대해 O-grid 코어 분할을 시도합니다.
        for i, feat in enumerate(parallel_major_cyls):
            # 격자 품질을 위해 원기둥은 무조건 O-grid를 추천합니다.
            plans.append(self._generate_ogrid_plan(body_data, feat, f"Core_{i}"))
            print(f" - Core O-grid added: {feat['type']}_{i} (r={feat['radius']:.2f})")

        # 3-4. 중심축 기준 십자 분할 (Sector Split)
        # [지능형 억제] 비대칭 피쳐가 있거나, 박스 기반이면 90도 분할은 위험하므로 금지합니다.
        if largest_cyl and not is_block_based and not is_perforated and not has_asymmetric_feature:
            origin = np.array(largest_cyl["origin"])
            plans.extend(self._generate_sector_split_plan(body_data, main_axis, origin))
        else:
            reason = "Asymmetric" if has_asymmetric_feature else ("Block-based" if is_block_based else "Perforated")
            print(f" - {reason} feature detected. Suppressing 90-deg Sector splits to prevent Boolean errors.")
            # 십자 분할 대신 안전한 H-grid나 Axial 분할만 수행
            if not is_perforated:
                plans.extend(self._generate_hgrid_plan(body_data, planes))
        
        # 3-4. 축 방향 단차 및 피쳐 격리 (Axial Split + Intelligent Merge)
        # 모든 주요 실린더/콘의 시작/끝 지점을 추적합니다. (막힌 구멍, 보스 포함)
        raw_z_splits = []
        axis_idx = np.argmax(np.abs(main_axis))
        
        # 부품의 전체 범위를 파악하여 '막힌' 구멍인지 판단하는 기준으로 사용
        all_min = np.min([f["box"]["min"][axis_idx] for f in faces], axis=0)
        all_max = np.max([f["box"]["max"][axis_idx] for f in faces], axis=0)
        
        for feat in major_cyls:
            z_min = feat["box"]["min"][axis_idx]
            z_max = feat["box"]["max"][axis_idx]
            
            # [지능형 단차 포착] 구멍이나 보스가 부품 끝까지 뚫려있지 않다면 그곳이 단차입니다.
            if not np.isclose(z_min, all_min, atol=1.0): raw_z_splits.append(z_min)
            if not np.isclose(z_max, all_max, atol=1.0): raw_z_splits.append(z_max)
            
        raw_z_splits.sort()
        # [핵심] 지능형 단차 병합: 0.5mm 이하의 미세한 틈은 하나로 합쳐서 슬리버 바디 방지
        merged_z = []
        if raw_z_splits:
            merged_z.append(raw_z_splits[0])
            for z in raw_z_splits[1:]:
                if z - merged_z[-1] > 0.5: # 0.5mm 병합 임계값
                    merged_z.append(z)
        
        # 중복 제거 및 유효 지점만 추가
        for z in merged_z:
            if not np.isclose(z, all_min, atol=1.0) and not np.isclose(z, all_max, atol=1.0):
                plans.append(self._generate_axial_split_plan(body_data, z, main_axis))
                print(f" - Feature Transition Split added at Z={z:.2f}")

        # 3-5. 대칭성 체크 및 조언 추가
        self._add_symmetry_advice(body_data, plans)

        strategy_name = "BOX_JUNCTION" if is_block_based else "AXISYMMETRIC"
        return strategy_name, self._apply_beta_options(plans, body_data)

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
        # 십자 교차점 위상 에러 회피를 위해 두 번째 절단면을 0.05mm 미세 이동
        # (0.01mm는 CAD 공차와 겹칠 위험이 있어 0.05mm로 상향)
        origin2 = origin1 + n1 * 0.05
        
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

    def _add_symmetry_advice(self, body_data, plans):
        """바운딩 박스 중심을 기반으로 대칭성 여부를 판단하여 조언을 추가합니다."""
        faces = body_data.get("faces", [])
        if not faces: return
        
        all_min = np.min([f["box"]["min"] for f in faces], axis=0)
        all_max = np.max([f["box"]["max"] for f in faces], axis=0)
        center = (all_min + all_max) / 2.0
        
        is_symmetric = np.all(np.isclose(center, 0, atol=0.1))
        if is_symmetric:
            advice = "[Symmetry Detected] 부품이 원점 기준 대칭입니다. 1/4 또는 1/8 모델만 사용하여 해석 시간을 단축하는 것을 권장합니다."
            for plan in plans:
                plan["symmetry_advice"] = advice

    def get_ai_advice(self, body_data):
        return "해당 형상은 분기점이 복잡합니다. 메인 바디와 연결된 파이프의 접합부를 기준으로 평면 분할을 먼저 시도하세요."
