# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face):
    data = {"id": 0, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        if hasattr(face, "Id"): data["id"] = face.Id
        shape = face.Shape if hasattr(face, "Shape") else face
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            # [v4.32] EvaluationAtParameter(0,0)를 사용해 절대 좌표 점을 직접 얻음
            try:
                eval_res = face.Evaluate(face.ParameterRange.Start)
                data["origin"] = [eval_res.Point.X, eval_res.Point.Y, eval_res.Point.Z]
                data["axis"] = [eval_res.Normal.X, eval_res.Normal.Y, eval_res.Normal.Z]
            except:
                f = geom.Frame
                data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
            
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                if hasattr(shape, "Orientation") and str(shape.Orientation) == "Reversed": data["is_internal"] = True
        
        from SpaceClaim.Api.V22.Geometry import Matrix
        bbox = face.GetBoundingBox(Matrix.Identity)
        data["box"]["min"] = [bbox.Min.X, bbox.Min.Y, bbox.Min.Z]
        data["box"]["max"] = [bbox.Max.X, bbox.Max.Y, bbox.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Scene-based Occurrence Extraction (v4.32) ---")
    all_bodies_data = []
    
    # [v4.32] Window.ActiveWindow.Scene을 통해 화면에 보이는 실제 Occurrence들을 가져옵니다.
    try:
        scene = Window.ActiveWindow.Scene
        bodies = list(scene.GetDescendants[IDesignBody]())
    except:
        # 실패 시 GetRootPart 백업
        bodies = list(GetRootPart().GetDescendants[IDesignBody]())
        
    print(" - Found {0} bodies in Scene".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            original_name = body.Name
            unique_name = "AUTO_BODY_" + str(i)
            # Occurrence의 이름을 바꾸면 Master 이름도 바뀔 수 있으나, 고유 식별을 위해 강행
            body.Name = unique_name
            body_data = {"body_index": i, "body_name": unique_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            all_bodies_data.append(body_data)
            print(" - [OK] Processed: {0}".format(unique_name))
        except Exception as e: print(" - [ERROR] {0}".format(str(e)))
            
    unit_str = "m"
    try: unit_str = str(GetRootPart().Document.Units.Length.Symbol)
    except: pass
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] Outer error: " + str(e))
