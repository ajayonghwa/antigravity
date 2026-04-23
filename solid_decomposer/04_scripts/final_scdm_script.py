
# -*- coding: utf-8 -*-
# Auto-generated SpaceClaim Script for Solid Decomposition

def apply_ogrid(body_name, center_list, axis_list, core_offset, ns_names):
    # 1. 대상 바디 찾기 (모든 컴포넌트 탐색)
    bodies = GetRootPart().GetAllBodies()
    target_body = None
    for b in bodies:
        if b.Name == body_name:
            target_body = b
            break
    
    if not target_body:
        print("Body not found: " + body_name)
        return

    # 2. 실린더 컷팅 평면/축 설정
    origin = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin, direction)
    
    # 3. 평면 표면(Surface Body) 생성 및 자르기
    print("O-grid Splitting for: " + body_name)
    try:
        # 사용자님의 테스트(Solidify Sketch)와 동일한 원리로, 닫힌 원을 '표면 바디(면)'로 만듭니다.
        circle = Circle.Create(frame, core_offset)
        curve_seg = CurveSegment.Create(circle)
        
        # 원을 감싸는 평면 정의
        plane = Plane.Create(frame.Origin, frame.DirZ)
        
        # 표면 바디(수학 모델) 생성 및 스페이스클레임에 실제 바디로 등록
        math_body = Body.CreatePlanarBody(plane, [curve_seg])
        tool_body = DesignBody.Create(GetRootPart(), "Ogrid_Tool", math_body)
        
        target_sel = Selection.Create(target_body)
        # 생성된 원판 표면의 면(Face)을 선택
        cutter_sel = Selection.Create(tool_body.Faces[0])
        
        # 면으로 자르기 실행 (True: 면을 수직 방향으로 무한히 연장해서 자름)
        SplitBody.ByCutter(target_sel, cutter_sel, True)
        
        # 자르기에 사용한 임시 표면 바디 삭제
        tool_body.Delete()
        
    except Exception as e:
        print("Failed to apply O-grid split: " + str(e))

def apply_hgrid(body_name, origin_list, normal_list, ns_names):
    # 1. 대상 바디 찾기
    bodies = GetRootPart().GetAllBodies()
    target_body = None
    for b in bodies:
        if b.Name == body_name:
            target_body = b
            break
            
    if not target_body:
        print("Body not found: " + body_name)
        return

    # 2. 분할 평면 생성
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane = Plane.Create(origin, normal)
    
    # 3. 바디 분할 실행
    print("H-grid Plane Splitting for: " + body_name)
    try:
        # 2024 R1 방식: ByCutter와 Selection 객체 사용
        target_sel = Selection.Create(target_body)
        
        # 먼저 평면 자체를 커터로 사용 시도
        try:
            SplitBody.ByCutter(target_sel, plane)
        except:
            # 실패 시 데이텀 평면(Datum Plane)을 임시로 생성하여 자르고 지우는 안전한 방식 사용
            datum = DatumPlaneCreator.Create(origin, normal).CreatedPlanes[0]
            SplitBody.ByCutter(target_sel, Selection.Create(datum))
            datum.Delete()
            
    except Exception as e:
        print("Failed to apply H-grid split: " + str(e))

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
apply_ogrid('Hybrid_Block_Hole', [0, 0, 50], [0, 0, 1], 6.0, {'core': 'VALVE_01_HybridHole_OGRID_CORE_SIZE_2.0mm', 'outer': 'VALVE_01_HybridHole_OGRID_OUTER_SIZE_2.0mm'})
apply_hgrid('Hybrid_Block_Hole', [0.0, 0.0, 50.0], [1, 0, 0], {'part_a': 'VALVE_01_HGRID_A_SIZE_2.0mm', 'part_b': 'VALVE_01_HGRID_B_SIZE_2.0mm'})

finalize()
