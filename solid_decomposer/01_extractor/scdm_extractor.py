# -*- coding: utf-8 -*-
import json
import os

def export_geometry_data(output_path):
    sub_device_name = "DEVICE"
    
    # 1. 문서 단위계 정보 획득 (중요!)
    unit_symbol = "m"
    try:
        unit_symbol = str(Window.ActiveWindow.ActiveContext.Units.Length.Symbol)
    except: pass
    
    data = {
        "sub_device_name": sub_device_name,
        "units": unit_symbol,
        "bodies": []
    }
    
    bodies = GetRootPart().GetAllBodies()
    for i, body in enumerate(bodies):
        # 바디 이름 (FullName 권장)
        b_name = body.Name
        try:
            fn = getattr(body, 'GetFullName', None)
            if fn: b_name = fn()
        except: pass
        
        body_info = {
            "body_index": i + 1,
            "body_name": b_name,
            "faces": []
        }
        
        for f_idx, face in enumerate(body.Faces):
            face_type = str(face.Geometry.Shape)
            face_data = {
                "index": f_idx,
                "type": face_type,
                "box": {
                    "min": [face.BoundingBox.Min.X, face.BoundingBox.Min.Y, face.BoundingBox.Min.Z],
                    "max": [face.BoundingBox.Max.X, face.BoundingBox.Max.Y, face.BoundingBox.Max.Z]
                }
            }
            
            # 실린더/콘 정보 추출
            if face_type in ["Cylinder", "Conical"]:
                surf = face.Geometry
                face_data["radius"] = surf.Radius
                face_data["origin"] = [surf.Frame.Origin.X, surf.Frame.Origin.Y, surf.Frame.Origin.Z]
                face_data["axis"] = [surf.Frame.Axis.Z.X, surf.Frame.Axis.Z.Y, surf.Frame.Axis.Z.Z]
                # 내부/외부 판단
                face_data["is_internal"] = face.IsInternal
            
            # 평면 정보
            elif face_type == "Plane":
                surf = face.Geometry
                face_data["origin"] = [surf.Frame.Origin.X, surf.Frame.Origin.Y, surf.Frame.Origin.Z]
                face_data["normal"] = [surf.Frame.Axis.Z.X, surf.Frame.Axis.Z.Y, surf.Frame.Axis.Z.Z]
                
            body_info["faces"].append(face_data)
        
        data["bodies"].append(body_info)
        
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print("Geometry data exported with units: " + unit_symbol)

# 스크립트 실행부
if __name__ == "__main__":
    export_geometry_data("geometry_data.json")
