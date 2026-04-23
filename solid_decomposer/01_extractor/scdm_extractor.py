# -*- coding: utf-8 -*-
import json
import os

# ==========================================
# [사용자 설정] 저장할 경로를 입력하세요. (마스터 스크립트 실행 시 자동 오버라이드됨)
if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face):
    """
    면(Face)의 기하학적 상세 정보를 추출합니다.
    """
    # V22 호환성을 위한 Shape/Geometry 접근
    shape = face
    try: shape = face.Shape
    except: pass
    
    geometry = None
    try: geometry = shape.Geometry
    except: pass
    
    data = {
        "id": getattr(face, 'Id', 0),
        "type": "Unknown",
        "area": getattr(shape, 'Area', 0),
        "box": {"min": [0,0,0], "max": [0,0,0]}
    }
    
    # Bounding Box 추출
    try:
        r = getattr(shape, 'Range', getattr(face, 'Box', getattr(face, 'BoundingBox', None)))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass

    if geometry:
        # 타입 판별 및 세부 파라미터 수집
        shape_type = str(geometry.GetType().Name)
        data["type"] = shape_type
        
        try:
            frame = getattr(geometry, 'Frame', None)
            
            # 실린더형 (Cylinder, Conical)
            if "Cylinder" in shape_type or "Conical" in shape_type:
                data["radius"] = getattr(geometry, 'Radius', 0)
                # 내경/외경 판별 로직 (Reversed Orientation 체크)
                is_internal = False
                try:
                    if hasattr(shape, 'Orientation') and str(shape.Orientation) == 'Reversed':
                        is_internal = True
                except: pass
                data["is_internal"] = is_internal
                
                if frame:
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
            
            # 평면형 (Plane)
            elif "Plane" in shape_type:
                if frame:
                    data["normal"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                    
            # 토로이달 (Toroidal - Elbow 등)
            elif "Toroidal" in shape_type:
                data["radius"] = getattr(geometry, 'MajorRadius', 0)
                data["minor_radius"] = getattr(geometry, 'MinorRadius', 0)
                if frame:
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
        except: pass
            
    return data

def extract_geometry():
    print("--- Starting Detailed Geometry Extraction (v3.4) ---")
    all_bodies_data = []
    warnings = []
    
    # 1. 시스템 단위(Units) 추출
    unit_str = "Unknown"
    try:
        # SpaceClaim API에서 활성 문서의 단위 설정 확인
        # V22에서는 Session.ActiveDocument.Units 등을 사용할 수도 있으나 GetRootPart 기반이 안전
        root = GetRootPart()
        # 일반적으로 SCDM 내부 연산은 Meter 기준이지만, 사용자 표시 단위 확인 시도
        try: unit_str = str(root.Document.Units.Length.Symbol)
        except: unit_str = "m (System Default)"
    except: pass
    print(" - Model Units Detected: {0}".format(unit_str))

    # 2. 모든 바디 수집 (재귀적 탐색)
    def get_all_bodies_recursive(part, body_list):
        for body in part.Bodies:
            body_list.append(body)
        for comp in part.Components:
            if comp.Template:
                get_all_bodies_recursive(comp.Template, body_list)

    bodies = []
    try:
        get_all_bodies_recursive(GetRootPart(), bodies)
    except Exception as e:
        print("Error during body collection: " + str(e))
        return [], [str(e)]
            
    print("Found {0} bodies in total.".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            # 바디 식별 이름 수집
            original_full_name = "Unknown"
            try: original_full_name = body.GetFullName().replace("\\", "/")
            except: 
                try: original_full_name = body.Name
                except: pass

            # 바디 고유 ID 부여 및 이름 변경 (추적 용도)
            unique_name = "AUTO_BODY_" + str(i)
            try: body.Name = unique_name
            except: pass

            # 기본 정보
            volume = 0
            try: volume = body.Shape.Volume
            except: 
                try: volume = body.Volume
                except: pass
                
            body_data = {
                "body_index": i,
                "body_name": unique_name,
                "original_name": original_full_name,
                "volume": volume,
                "faces": [],
                "adjacency": [],
                "identified_holes": []
            }
            
            # 면 상세 정보 추출
            face_map = {}
            faces = []
            try: faces = list(body.Faces)
            except: 
                try: faces = list(body.Shape.Faces)
                except: pass
                
            for j, face in enumerate(faces):
                f_data = get_face_data(face)
                f_data["index"] = j
                body_data["faces"].append(f_data)
                face_map[face] = j
                
            # 면 간 인접성 추출
            try:
                edges = []
                try: edges = body.Edges
                except: edges = body.Shape.Edges
                
                for edge in edges:
                    adj_faces = edge.Faces
                    if adj_faces.Count == 2:
                        idx1 = face_map.get(adj_faces[0])
                        idx2 = face_map.get(adj_faces[1])
                        if idx1 is not None and idx2 is not None:
                            body_data["adjacency"].append([idx1, idx2])
            except: pass
            
            # 물리적 홀 식별 (IdentifyHoles API 활용)
            try:
                from SpaceClaim.Api.V22.Modeler import IdentifyHoleOptions
                holes = body.IdentifyHoles(IdentifyHoleOptions())
                for hole in holes:
                    hole_data = {
                        "type": "Through" if hole.Through else "Blind",
                        "diameter": hole.DrillSize,
                        "depth": hole.Depth,
                        "has_counterbore": hole.Counterbore is not None,
                        "has_countersink": hole.Countersink is not None
                    }
                    try:
                        hole_data["axis"] = [hole.Axis.Direction.X, hole.Axis.Direction.Y, hole.Axis.Direction.Z]
                        hole_data["origin"] = [hole.Axis.Origin.X, hole.Axis.Origin.Y, hole.Axis.Origin.Z]
                    except: pass
                    body_data["identified_holes"].append(hole_data)
            except: pass
                    
            all_bodies_data.append(body_data)
            print(" - [Success] Extracted Body: {0} ({1} faces)".format(unique_name, len(body_data["faces"])))
            
        except Exception as e:
            msg = "Failed to process body {0}: {1}".format(i, str(e))
            print(" !! " + msg)
            warnings.append(msg)
            continue
        
    return all_bodies_data, warnings, unit_str

# 메인 실행
try:
    results, warnings, unit_info = extract_geometry()
    
    final_data = {
        "sub_device_name": "DEVICE",
        "units": unit_info,
        "warnings": warnings,
        "bodies": results
    }
    
    # 폴더 자동 생성 및 저장
    target_dir = os.path.dirname(OUTPUT_PATH)
    if target_dir and not os.path.exists(target_dir): os.makedirs(target_dir)
        
    with open(OUTPUT_PATH, "w") as f:
        json.dump(final_data, f, indent=2)
    print("\n[Result] Geometry data saved to: " + OUTPUT_PATH)
except Exception as e:
    print("\n[Critical Error] Extraction failed: " + str(e))
