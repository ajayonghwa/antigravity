# -*- coding: utf-8 -*-
import json
import os

def export_geometry_data():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data")
    
    if not os.path.exists(data_dir):
        try: os.makedirs(data_dir)
        except: data_dir = os.getcwd()
        
    output_path = os.path.join(data_dir, "geometry_data_block.json")
    
    data = {
        "sub_device_name": "DEVICE",
        "units": "m",
        "bodies": []
    }
    
    try:
        bodies = GetRootPart().GetAllBodies()
    except:
        print("Error: Could not get bodies.")
        return

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
                    # [핵심 수정] DesignFace와 일반 Face 모두 대응
                    # DesignFace는 .Shape를 거쳐야 Geometry에 접근 가능합니다.
                    target_face = face
                    if hasattr(face, "Shape"):
                        target_face = face.Shape
                    
                    geom = target_face.Geometry
                    if not geom: continue
                    
                    # 타입 판별
                    face_type = "Unknown"
                    try:
                        face_type = geom.GetType().Name
                        if hasattr(geom, "Shape"): # GeometryShape Enum
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
                        face_data["is_internal"] = target_face.IsInternal # Face 객체에서 추출
                    elif "Plane" in face_type:
                        face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                        face_data["normal"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                        
                    body_info["faces"].append(face_data)
                except Exception as e:
                    # print("Face error: " + str(e))
                    continue
            
            body_info["face_count"] = len(body_info["faces"])
            data["bodies"].append(body_info)
        except:
            continue
            
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print("Success! Data saved to: " + output_path)

if __name__ == "__main__":
    export_geometry_data()
