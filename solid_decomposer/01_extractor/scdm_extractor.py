# -*- coding: utf-8 -*-
import json
import os

# ==========================================
# [사용자 설정] 저장할 경로를 입력하세요.
# 예: r"C:\Projects\antigravity\solid_decomposer\data\geometry_data_block.json"
# ==========================================
OUTPUT_PATH = r"C:\path\to\your\data\geometry_data_block.json"

def get_face_data(face):
    """
    사용자님의 검증 로직(Normal/Radial)과 DesignFace 호환성을 결합한 핵심 추출 함수
    """
    # 1. DesignFace/Face 대응
    target_face = face
    if hasattr(face, "Shape"):
        target_face = face.Shape
    
    geometry = getattr(target_face, 'Geometry', None)
    
    data = {
        "index": 0, # 외부에서 부여
        "type": "Unknown",
        "area": getattr(target_face, 'Area', 0),
        "box": {
            "min": [face.BoundingBox.Min.X, face.BoundingBox.Min.Y, face.BoundingBox.Min.Z],
            "max": [face.BoundingBox.Max.X, face.BoundingBox.Max.Y, face.BoundingBox.Max.Z]
        }
    }
    
    if geometry:
        # 타입 판별
        shape_type = str(getattr(geometry, 'Shape', geometry.GetType().Name))
        data["type"] = shape_type
        
        try:
            frame = getattr(geometry, 'Frame', None)
            
            # 실린더(Cylinder) 정보 추출 및 사용자 Validator 적용
            if "Cylinder" in shape_type or "Conical" in shape_type:
                data["radius"] = getattr(geometry, 'Radius', 0)
                data["is_internal"] = getattr(target_face, 'IsInternal', False)
                
                if frame:
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                
                # --- [사용자님 Validator 로직 복구] ---
                try:
                    # 1순위: 면의 방향성(Orientation) 확인
                    if hasattr(target_face, 'Orientation') and str(target_face.Orientation) == 'Reversed':
                        data["is_internal"] = True
                    else:
                        # 2순위: 법선 벡터와 방사 벡터의 내적 확인 (Hole 검증)
                        try:
                            # 0.5, 0.5 지점의 법선 벡터 추출
                            param = Parameter.Create(0.5, 0.5)
                            normal = target_face.NormalAt(param)
                            center = target_face.Box.Center
                            # 방사 벡터 (Z축 제외 XY 평면 기준)
                            radial = Vector.Create(center.X, center.Y, 0).Direction
                            if Vector.Dot(radial, normal) < -0.1:
                                data["is_internal"] = True
                        except: pass
                except: pass
                # ------------------------------------
            
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
        except:
            pass
            
    return data

def export_geometry_data():
    print("--- Starting Ultimate Greedy Extraction ---")
    
    data = {
        "sub_device_name": "DEVICE",
        "units": "m",
        "bodies": []
    }
    
    try:
        bodies = GetRootPart().GetAllBodies()
    except:
        print("Error: Accessing bodies failed.")
        return

    for i, body in enumerate(bodies):
        try:
            # 바디 이름 및 부피 추출
            body_name = "Body_" + str(i)
            try:
                fn = getattr(body, 'GetFullName', None)
                body_name = fn() if fn else body.Name
            except: pass
            
            volume = getattr(body, 'Volume', 0)
            if hasattr(body, 'Shape'): volume = getattr(body.Shape, 'Volume', volume)
                
            body_info = {
                "body_index": i,
                "body_name": body_name,
                "volume": volume,
                "faces": []
            }
            
            # 면 정보 추출
            faces = getattr(body, 'Faces', [])
            for j, face in enumerate(faces):
                try:
                    f_data = get_face_data(face)
                    f_data["index"] = j
                    body_info["faces"].append(f_data)
                except: continue
            
            data["bodies"].append(body_info)
            print(" - Body {0} extracted: {1} ({2} faces)".format(i, body_name, len(body_info["faces"])))
        except:
            continue
            
    # 파일 저장
    try:
        target_dir = os.path.dirname(OUTPUT_PATH)
        if target_dir and not os.path.exists(target_dir): os.makedirs(target_dir)
            
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print("--- All Data Saved Successfully! ---")
        print("Path: " + OUTPUT_PATH)
    except Exception as e:
        print("Save failed: " + str(e))

if __name__ == "__main__":
    export_geometry_data()
