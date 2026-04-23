# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face):
    # [v4.34] 투명성을 위해 try-except 제거
    from SpaceClaim.Api.V22.Geometry import Matrix
    data = {"id": face.Id, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    
    shape = face.Shape
    if hasattr(shape, "Geometry"):
        geom = shape.Geometry
        g_type = geom.GetType().Name
        data["type"] = g_type
        
        # Occurrence 기준 절대 좌표 추출
        eval_res = face.Evaluate(face.ParameterRange.Start)
        data["origin"] = [eval_res.Point.X, eval_res.Point.Y, eval_res.Point.Z]
        data["axis"] = [eval_res.Normal.X, eval_res.Normal.Y, eval_res.Normal.Z]
        
        if "Cylinder" in g_type or "Conical" in g_type:
            data["radius"] = getattr(geom, "Radius", 0.0)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
    
    bbox = face.GetBoundingBox(Matrix.Identity)
    data["box"]["min"] = [bbox.Min.X, bbox.Min.Y, bbox.Min.Z]
    data["box"]["max"] = [bbox.Max.X, bbox.Max.Y, bbox.Max.Z]
    return data

def extract_geometry():
    print("--- SCDM Transparent Extraction (v4.34) ---")
    all_bodies_data = []
    
    # [v4.34] 현재 창에 보이는 모든 Occurrence 바디 수집
    scene = Window.ActiveWindow.Scene
    bodies = list(scene.GetDescendants[IDesignBody]())
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        original_name = body.Name
        unique_name = "AUTO_BODY_" + str(i)
        
        # [v4.34] RenameInstance 명령어로 읽기 전용 무시하고 강제 이름 변경
        try:
            RenameInstance.Execute(Selection.Create(body), unique_name)
        except:
            # 실패 시 직접 대입 시도
            body.Name = unique_name
        
        actual_name = body.Name
        body_data = {"body_index": i, "body_name": actual_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
        for j, face in enumerate(list(body.Faces)):
            fdata = get_face_data(face)
            fdata["index"] = j
            body_data["faces"].append(fdata)
        all_bodies_data.append(body_data)
        print(" - [OK] {0} -> {1}".format(original_name, actual_name))
            
    unit_str = str(GetRootPart().Document.Units.Length.Symbol)
    return all_bodies_data, [], unit_str

results, warns, uinfo = extract_geometry()
final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
print("\n[FINISH] Geometry data saved.")
