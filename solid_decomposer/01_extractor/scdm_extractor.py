# -*- coding: utf-8 -*-
import json
import os

# ==========================================
# [사용자 설정] 저장할 경로를 입력하세요.
# 예: r"C:\Users\yonghwaheo\Documents\antigravity\solid_decomposer\data\geometry_data_block.json"
# ==========================================
OUTPUT_PATH = r"C:\path\to\your\data\geometry_data_block.json"

def get_face_data(face):
    """
    사용자님의 어제자 성공 코드를 기반으로 한 면(Face) 정보 추출 로직
    """
    # DesignFace 호환성 (오늘의 핵심 수정)
    shape = face.Shape if hasattr(face, "Shape") else face
    geometry = getattr(shape, 'Geometry', None)
    
    data = {
        "id": getattr(face, 'Id', 0),
        "type": "Unknown",
        "area": getattr(shape, 'Area', 0),
        "box": {"min": [0,0,0], "max": [0,0,0]}
    }
    
    # 바운딩 박스
    try:
        r = getattr(shape, 'Range', getattr(face, 'Box', getattr(face, 'BoundingBox', None)))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass

    if geometry:
        # 타입 판별
        shape_type = str(getattr(geometry, 'Shape', geometry.GetType().Name))
        data["type"] = shape_type
        
        try:
            frame = getattr(geometry, 'Frame', None)
            
            # 실린더(Cylinder) 및 내경 판별
            if "Cylinder" in shape_type or "Conical" in shape_type:
                data["radius"] = getattr(geometry, 'Radius', 0)
                data["is_internal"] = getattr(shape, 'IsInternal', False)
                
                if frame:
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                
                # --- 사용자님 전용 Validator 복구 ---
                try:
                    if hasattr(shape, 'Orientation') and str(shape.Orientation) == 'Reversed':
                        data["is_internal"] = True
                    else:
                        try:
                            # 법선 벡터 평가를 통한 Hole 검증
                            # SpaceClaim API의 Parameter/Vector 객체 사용
                            param = Parameter.Create(0.5, 0.5)
                            normal = shape.NormalAt(param)
                            bbox = getattr(shape, 'Box', getattr(shape, 'BoundingBox', None))
                            if bbox:
                                center = bbox.Center
                                radial = Vector.Create(center.X, center.Y, 0).Direction
                                if Vector.Dot(radial, normal) < -0.1:
                                    data["is_internal"] = True
                        except: pass
                except: pass
            
            # 평면(Plane)
            elif "Plane" in shape_type:
                if frame:
                    data["normal"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                
            # 토로이달(Toroidal)
            elif "Toroidal" in shape_type:
                data["radius"] = getattr(geometry, 'MajorRadius', 0)
                data["minor_radius"] = getattr(geometry, 'MinorRadius', 0)
                if frame:
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
        except: pass
            
    return data

def extract_geometry():
    print("--- Starting Full Geometry Extraction ---")
    all_bodies_data = []
    
    # 1. 대상 바디 수집 (성공했던 Fallback 로직 복구)
    try:
        root = GetRootPart()
        bodies = root.GetAllBodies()
    except:
        try: bodies = GetRootPart().Bodies
        except:
            print("Error: Could not find any bodies.")
            return []
            
    print("Found {0} bodies.".format(bodies.Count))

    for i, body in enumerate(bodies):
        try:
            body_name = "Body_" + str(i)
            fn = getattr(body, 'GetFullName', None)
            if fn: body_name = fn()
            elif hasattr(body, 'Name'): body_name = body.Name
            
            volume = getattr(body, 'Volume', 0)
            if hasattr(body, 'Shape'): volume = getattr(body.Shape, 'Volume', volume)

            body_data = {
                "body_index": i,
                "body_name": body_name,
                "volume": volume,
                "faces": [],
                "adjacency": [] # Planner에서 필요할 수 있음
            }
            
            # 면 정보 추출
            faces = getattr(body, 'Faces', [])
            face_map = {}
            for j, face in enumerate(faces):
                f_data = get_face_data(face)
                f_data["index"] = j
                body_data["faces"].append(f_data)
                face_map[face] = j
                
            # 인접성(Adjacency) 추출 (원래 있던 기능 복구)
            try:
                edges = getattr(body, 'Edges', [])
                for edge in edges:
                    adj_faces = getattr(edge, 'Faces', [])
                    if hasattr(adj_faces, 'Count') and adj_faces.Count == 2:
                        idx1 = face_map.get(adj_faces[0])
                        idx2 = face_map.get(adj_faces[1])
                        if idx1 is not None and idx2 is not None:
                            body_data["adjacency"].append([idx1, idx2])
            except: pass
                    
            all_bodies_data.append(body_data)
            print(" - Processed: {0}".format(body_name))
        except: continue
        
    return all_bodies_data

# 메인 실행부
try:
    results = extract_geometry()
    
    # 파이프라인 호환용 래핑 구조
    final_data = {
        "sub_device_name": "DEVICE",
        "units": "m",
        "bodies": results
    }
    
    # 폴더 자동 생성
    target_dir = os.path.dirname(OUTPUT_PATH)
    if target_dir and not os.path.exists(target_dir): os.makedirs(target_dir)
        
    with open(OUTPUT_PATH, "w") as f:
        json.dump(final_data, f, indent=2)
        
    print("--- SUCCESS: " + OUTPUT_PATH + " ---")
except Exception as e:
    print("FATAL ERROR: " + str(e))
