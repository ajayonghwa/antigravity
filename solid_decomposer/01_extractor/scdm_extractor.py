# -*- coding: utf-8 -*-
import json
import os

def export_geometry_data():
    # 1. 저장할 파일명 (스페이스클레임에서 실행 시 현재 활성 문서와 같은 경로에 생깁니다)
    output_path = "geometry_data.json"
    
    data = {
        "sub_device_name": "DEVICE",
        "units": "m", # 기본값
        "bodies": []
    }
    
    # 2. 바디 순회 및 추출
    bodies = GetRootPart().GetAllBodies()
    for i, body in enumerate(bodies):
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
            shape = str(face.Geometry.Shape)
            face_data = {
                "index": f_idx,
                "type": shape,
                "box": {
                    "min": [face.BoundingBox.Min.X, face.BoundingBox.Min.Y, face.BoundingBox.Min.Z],
                    "max": [face.BoundingBox.Max.X, face.BoundingBox.Max.Y, face.BoundingBox.Max.Z]
                }
            }
            
            # 실린더, 콘, 평면 정보 추출
            geom = face.Geometry
            if shape in ["Cylinder", "Conical"]:
                face_data["radius"] = geom.Radius
                face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                face_data["axis"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                face_data["is_internal"] = face.IsInternal
            elif shape == "Plane":
                face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                face_data["normal"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                
            body_info["faces"].append(face_data)
        
        data["bodies"].append(body_info)
        
    # 3. 파일 쓰기
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print("Export finished! File saved as: " + os.path.abspath(output_path))

# 실행
export_geometry_data()
