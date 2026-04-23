
# -*- coding: utf-8 -*-
# Auto-generated SpaceClaim Script for Solid Decomposition
import clr
import System

def apply_ogrid(body_name, center_list, axis_list, core_offset, ns_names):
    # 1. 대상 바디들 찾기 (원본 이름과 일치하거나 분할로 인해 숫자가 붙은 모든 조각들 수집)
    bodies = GetRootPart().GetAllBodies()
    target_bodies = []
    for b in bodies:
        b_name = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_name = fn()
        except:
            pass
        
        # [핵심 수정] 엄격한 이름 매칭 (이웃 바디 오절단 방지)
        is_match = False
        if b_name == body_name:
            is_match = True
        elif b_name.startswith(body_name + " ("):
            is_match = True
        elif b_name.startswith(body_name + " "):
            is_match = True
        
        if is_match:
            target_bodies.append(b)
    
    if not target_bodies:
        print("Body not found: " + body_name)
        return

    # 2. 모든 대상 조각에 대해 분할 시도 (평면이 지나는 조각만 실제로 잘림)
    for target_body in target_bodies:
        # 2. 실린더 컷팅 평면/축 설정
        origin = Point.Create(center_list[0], center_list[1], center_list[2])
        direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
        frame = Frame.Create(origin, direction)

        tool_body = None
        try:
            # 3. 평면 표면(Surface Body) 생성 및 자르기
            print("O-grid Splitting for piece of: " + body_name)
            circle = Circle.Create(frame, core_offset)
            curve_seg = CurveSegment.Create(circle)
            
            # 원을 감싸는 평면 정의 (Plane.Create는 1개의 Frame 인수를 받음)
            plane = Plane.Create(frame)
            
            # Python의 list([]) 대신 .NET의 Array를 명시적으로 생성하여 전달합니다. (타입 에러 방지)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            
            # 표면 바디(수학 모델) 생성 및 스페이스클레임에 실제 바디로 등록
            math_body = Body.CreatePlanarBody(plane, curve_array)
            tool_body = DesignBody.Create(GetRootPart(), "Ogrid_Tool", math_body)
            
            target_sel = Selection.Create(target_body)
            # 생성된 원판 표면의 면(Face)을 선택
            cutter_sel = Selection.Create(tool_body.Faces[0])
            
            # 면으로 자르기 실행 (실패하더라도 다음 조각으로 넘어가야 함)
            try:
                res = SplitBody.ByCutter(target_sel, cutter_sel, True)
                
                # 분할 성공 시 네임드 셀렉션 부여 (Core / Outer 구분)
                if res and res.Success and res.CreatedBodies.Count >= 2:
                    core_bodies = []
                    outer_bodies = []
                    for cb in res.CreatedBodies:
                        cg = cb.GetBoundingBox(Matrix.Identity).Center
                        # Z축 방향을 제외한 반경(Radial) 거리로 구분
                        dist = ((cg.X - origin.X)**2 + (cg.Y - origin.Y)**2)**0.5
                        if dist < core_offset:
                            core_bodies.append(cb)
                        else:
                            outer_bodies.append(cb)
                    
                    try:
                        if core_bodies and "core" in ns_names:
                            Selection.Create(core_bodies).CreateGroup(ns_names["core"])
                        if outer_bodies and "outer" in ns_names:
                            Selection.Create(outer_bodies).CreateGroup(ns_names["outer"])
                    except: pass
            except:
                pass
            
        except Exception as e:
            print("O-grid error: " + str(e))
        finally:
            # 성공/실패 여부와 상관없이 임시 도구는 반드시 삭제
            if tool_body:
                tool_body.Delete()

def apply_hgrid(body_name, origin_list, normal_list, ns_names):
    # 1. 대상 바디들 찾기 (분할된 조각들까지 모두 수집)
    bodies = GetRootPart().GetAllBodies()
    target_bodies = []
    for b in bodies:
        b_name = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_name = fn()
        except: pass
        
        base = b_name.split("/")[-1]
        
        # [핵심 수정] 엄격한 이름 매칭 (이웃 바디 오절단 방지)
        is_match = False
        if base == body_name:
            is_match = True
        elif base.startswith(body_name + " ("): # "Body (1)" 형태 매칭
            is_match = True
        elif base.startswith(body_name + " "): # "Body 1" 형태 매칭
            is_match = True
        
        if is_match:
            target_bodies.append(b)
            
    if not target_bodies:
        print("Body not found: " + body_name)
        return

    # 2. 분할 평면 생성
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane = Plane.Create(Frame.Create(origin, normal))
    
    # 3. [핵심 수정] 일괄 분할 대신 '순차적 분할'로 조각 누락 방지
    print("Sequential Splitting fragments of: " + body_name)
    all_new_fragments = []
    
    for target in target_bodies:
        try:
            # 개별 바디에 대해 분할 실행
            res = SplitBody.ByCutter(Selection.Create(target), plane)
            if res and res.Success:
                all_new_fragments.extend([cb for cb in res.CreatedBodies])
            else:
                all_new_fragments.append(target) # 잘리지 않은 경우 유지
        except:
            all_new_fragments.append(target)

    # 4. 네임드 셀렉션 부여 (생성된 모든 조각 대상)
    if all_new_fragments and ns_names:
        mid = len(all_new_fragments) // 2
        try:
            if "part_a" in ns_names: Selection.Create(all_new_fragments[:mid]).CreateGroup(ns_names["part_a"])
            if "part_b" in ns_names: Selection.Create(all_new_fragments[mid:]).CreateGroup(ns_names["part_b"])
        except: pass


def apply_sector(body_name, origin_list, normal_list, ns_names):
    # 90도 십자 분할을 위한 전용 함수
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane = Plane.Create(Frame.Create(origin, normal))
    
    bodies = GetRootPart().GetAllBodies()
    for b in bodies:
        if b.Name.startswith(body_name):
            try:
                SplitBody.ByCutter(Selection.Create(b), plane)
            except: pass

def finalize():
    print("Applying Shared Topology for Conformal Meshing...")
    try:
        # 1. 파트 속성 방식 (일반적인 접근)
        GetRootPart().SharedTopology = PartSharedTopology.Share
    except:
        pass
        
    try:
        # 2. 스페이스클레임 도구 실행 방식 (2024 R1에서 직접 자른 후 강제 적용)
        options = ShareTopologyOptions()
        options.Tolerance = MM(0.2)
        # Info 자리에 None이나 빈 Selection을 주면 전체 대상
        ShareTopology.FindAndFix(options, None)
    except Exception as e:
        print("ShareTopology Fix failed (might not be necessary): " + str(e))
        
    print("All operations completed successfully.")

# --- Execution ---
apply_ogrid('Debug_Cylinder', [0, 0, 50], [0, 0, 1], 24.0, {'core': 'DEBUG_RUN_Core_0_OGRID_CORE_SIZE_8.0mm', 'outer': 'DEBUG_RUN_Core_0_OGRID_OUTER_SIZE_8.0mm'})
apply_sector('Debug_Cylinder', [0.0, 0.0, 50.0], [1.0, 0.0, 0.0], {'part_a': 'DEBUG_RUN_SEC1_A_SIZE_2.0mm', 'part_b': 'DEBUG_RUN_SEC1_B_SIZE_2.0mm'})
apply_sector('Debug_Cylinder', [0.01, 0.0, 50.0], [0.0, 1.0, 0.0], {'part_a': 'DEBUG_RUN_SEC2_A_SIZE_2.0mm', 'part_b': 'DEBUG_RUN_SEC2_B_SIZE_2.0mm'})

finalize()
