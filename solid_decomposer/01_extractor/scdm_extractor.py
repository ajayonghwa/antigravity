# -*- coding: utf-8 -*-
# SpaceClaim IronPython Script for Geometry Extraction
import json
import os

# === Configuration ===
output_dir = r"C:\Temp\SCDM_Export" # 기본 경로, 필요시 수정
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, "geometry_data.json")

def get_face_data(face):
    """
    면(Face)의 기하학적 정보를 안전하게 추출합니다.
    Ansys 2024 R1 (SpaceClaim) API 호환성을 높였습니다.
    """
    shape = getattr(face, 'Shape', face)
    geometry = getattr(shape, 'Geometry', None)
    
    data = {
        "id": getattr(face, 'Id', 0),
        "type": "Unknown",
        "area": getattr(shape, 'Area', 0),
        "box": {"min": [0,0,0], "max": [0,0,0]}
    }
    
    # 1. 바운딩 박스 추출
    try:
        r = getattr(shape, 'Range', getattr(face, 'Box', None))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass

    # 2. 상세 기하 정보 추출
    if geometry:
        shape_type = str(getattr(geometry, 'Shape', type(geometry).__name__))
        data["type"] = shape_type
        
        try:
            # 안전한 Frame 속성 가져오기
            frame = getattr(geometry, 'Frame', None)
            
            # 실린더(Cylinder) 정보
            if "Cylinder" in shape_type:
                data["radius"] = getattr(geometry, 'Radius', 0)
                data["is_internal"] = False # 기본값: 외부 경계(Solid)
                
                if frame:
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                
                # 내경(Hole) 판별 로직 (CadQuery 검증 로직 이식)
                try:
                    # 1순위: 면의 방향성(Orientation) 확인
                    if hasattr(face, 'Orientation') and str(face.Orientation) == 'Reversed':
                        data["is_internal"] = True
                    else:
                        # 2순위: 법선 벡터(Normal)와 방사 벡터(Radial)의 내적(Dot Product) 확인
                        # SpaceClaim IronPython 내장 객체 활용
                        try:
                            param = Parameter.Create(0.5, 0.5)
                            normal = face.NormalAt(param)
                            center = face.Box.Center
                            radial = Vector.Create(center.X, center.Y, 0).Direction
                            if Vector.Dot(radial, normal) < -0.1:
                                data["is_internal"] = True
                        except: pass
                except: pass
            
            # 평면(Plane) 정보
            elif "Plane" in shape_type:
                if frame:
                    data["normal"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                
            # 토로이달(Toroidal) 정보 (엘보우 파이프 등)
            elif "Toroidal" in shape_type:
                data["radius"] = getattr(geometry, 'MajorRadius', 0)
                data["minor_radius"] = getattr(geometry, 'MinorRadius', 0)
                if frame:
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
            
            # 원뿔(Conical) 정보 (테이퍼 대응)
            elif "Conical" in shape_type:
                data["type"] = "Conical"
                # 테이퍼 구간은 시작과 끝의 반지름이 다름
                data["radius"] = getattr(geometry, 'Radius', 0)
                data["half_angle"] = getattr(geometry, 'HalfAngle', 0)
                if frame:
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
        except:
            pass
            
    return data

def extract_geometry():
    all_bodies_data = []
    
    # 1. 대상 바디 수집 (모든 하위 컴포넌트 포함)
    try:
        bodies = GetRootPart().GetAllBodies()
        count = bodies.Count
    except:
        # GetAllBodies가 실패할 경우 기본 Bodies로 대체 시도
        bodies = GetRootPart().Bodies
        count = bodies.Count
        
    print("Found " + str(count) + " bodies in the assembly.")

    for i, body in enumerate(bodies):
        # 바디 이름 안전하게 가져오기 (GetFullName 사용하여 중복 방지)
        body_name = "Body_" + str(i)
        try:
            # FullName은 "Component1/Body1" 처럼 경로를 모두 포함하여 유니크합니다.
            full_name = getattr(body, 'GetFullName', None)
            if full_name:
                body_name = full_name()
            elif hasattr(body, 'Name') and body.Name:
                body_name = body.Name
        except:
            pass
            
        # 부피 안전하게 가져오기
        volume = 0
        try:
            if hasattr(body, 'Volume'):
                volume = body.Volume
            elif hasattr(body, 'Shape') and hasattr(body.Shape, 'Volume'):
                volume = body.Shape.Volume
        except:
            pass

        body_data = {
            "body_index": i,
            "body_name": body_name,
            "volume": volume,
            "faces": [],
            "adjacency": []
        }
        
        # Extract Face Data
        try:
            faces = getattr(body, 'Faces', [])
            face_map = {} # To store index mapping
            for j, face in enumerate(faces):
                f_data = get_face_data(face)
                f_data["index"] = j
                body_data["faces"].append(f_data)
                face_map[face] = j
                
            # Extract Adjacency (Faces sharing an edge)
            edges = getattr(body, 'Edges', [])
            for edge in edges:
                adj_faces = getattr(edge, 'Faces', [])
                if hasattr(adj_faces, 'Count') and adj_faces.Count == 2:
                    idx1 = face_map.get(adj_faces[0])
                    idx2 = face_map.get(adj_faces[1])
                    if idx1 is not None and idx2 is not None:
                        body_data["adjacency"].append([idx1, idx2])
        except:
            pass
                    
        all_bodies_data.append(body_data)
        
    return all_bodies_data

# Main Execution
try:
    data = extract_geometry()
    
    # Ansys 2024 R1의 IronPython 환경에 최적화된 내장 json 사용
    json_text = json.dumps(data, indent=2)
    
    with open(output_file, "w") as f:
        f.write(json_text)
        
    print("Extraction successful: " + output_file)
except Exception as e:
    print("Error during extraction: " + str(e))
