# -*- coding: utf-8 -*-
import json
import os

# ==========================================
# [사용자 설정] 저장할 경로를 아래에 입력하세요.
# 예: r"C:\Projects\antigravity\solid_decomposer\data\geometry_data_block.json"
# ==========================================
OUTPUT_PATH = r"C:\path\to\your\data\geometry_data_block.json"

def export_geometry_data():
    print("--- Starting Geometry Extraction ---")
    
    data = {
        "sub_device_name": "DEVICE",
        "units": "m",
        "bodies": []
    }
    
    # 1. 바디 목록 가져오기
    try:
        bodies = GetRootPart().GetAllBodies()
        print("Found {0} bodies in Root Part.".format(bodies.Count))
    except Exception as e:
        print("Error: Could not access Root Part bodies. " + str(e))
        return

    # 2. 바디 순회
    for i, body in enumerate(bodies):
        try:
            b_name = body.Name
            try:
                if hasattr(body, 'GetFullName'): b_name = body.GetFullName()
            except: pass
                
            body_info = {
                "body_index": i + 1,
                "body_name": b_name,
                "faces": []
            }
            
            for f_idx, face in enumerate(body.Faces):
                try:
                    # DesignFace와 일반 Face 모두 대응
                    target_face = face
                    if hasattr(face, "Shape"):
                        target_face = face.Shape
                    
                    geom = target_face.Geometry
                    if not geom: continue
                    
                    # 타입 판별 (Enum 혹은 ClassName)
                    face_type = "Unknown"
                    try:
                        face_type = geom.GetType().Name
                        if hasattr(geom, "Shape"):
                            face_type = str(geom.Shape)
                    except: pass
                    
                    face_data = {
                        "index": f_idx,
                        "type": face_type,
                        "box": {
                            "min": [face.BoundingBox.Min.X, face.BoundingBox.Min.Y, face.BoundingBox.Min.Z],
                            "max": [face.BoundingBox.Max.X, face.BoundingBox.Max.Y, face.BoundingBox.Max.Z]
                        }
                    }
                    
                    # 실린더/평면 정보 추출
                    if "Cylinder" in face_type or "Conical" in face_type:
                        face_data["radius"] = geom.Radius
                        face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                        face_data["axis"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                        face_data["is_internal"] = target_face.IsInternal
                    elif "Plane" in face_type:
                        face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                        face_data["normal"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                        
                    body_info["faces"].append(face_data)
                except:
                    continue
            
            body_info["face_count"] = len(body_info["faces"])
            data["bodies"].append(body_info)
            print(" - Processed Body {0}: {1}".format(i+1, b_name))
        except:
            continue
            
    # 3. 파일 저장
    try:
        # 폴더가 없으면 생성 시도
        target_dir = os.path.dirname(OUTPUT_PATH)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print("--- Extraction Finished! ---")
        print("Saved to: " + OUTPUT_PATH)
    except Exception as e:
        print("Failed to save file: " + str(e))

# 실행
export_geometry_data()
