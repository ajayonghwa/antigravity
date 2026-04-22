# -*- coding: utf-8 -*-
import json
import os

def export_geometry_data():
    output_path = "geometry_data.json"
    
    data = {
        "sub_device_name": "DEVICE",
        "units": "m",
        "bodies": []
    }
    
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
            # [안전한 형상 타입 추출]
            geom = face.Geometry
            if not geom: continue
            
            # 1. Shape 속성 시도 -> 2. 클래스 이름 시도 (가장 확실함)
            face_type = "Unknown"
            try:
                if hasattr(geom, "Shape"):
                    face_type = str(geom.Shape)
                else:
                    face_type = geom.GetType().Name
            except:
                face_type = geom.GetType().Name
            
            face_data = {
                "index": f_idx,
                "type": face_type,
                "box": {
                    "min": [face.BoundingBox.Min.X, face.BoundingBox.Min.Y, face.BoundingBox.Min.Z],
                    "max": [face.BoundingBox.Max.X, face.BoundingBox.Max.Y, face.BoundingBox.Max.Z]
                }
            }
            
            # 실린더, 콘, 평면 정보 추출 (이름 매칭 유연화)
            if "Cylinder" in face_type or "Conical" in face_type:
                face_data["radius"] = geom.Radius
                face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                face_data["axis"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                face_data["is_internal"] = face.IsInternal
            elif "Plane" in face_type:
                face_data["origin"] = [geom.Frame.Origin.X, geom.Frame.Origin.Y, geom.Frame.Origin.Z]
                face_data["normal"] = [geom.Frame.Axis.Z.X, geom.Frame.Axis.Z.Y, geom.Frame.Axis.Z.Z]
                
            body_info["faces"].append(face_data)
        
        data["bodies"].append(body_info)
        
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print("Export finished! File saved as: " + os.path.abspath(output_path))

export_geometry_data()
