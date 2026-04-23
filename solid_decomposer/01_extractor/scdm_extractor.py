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
    print("--- SCDM Robust Renaming & Scene Extraction (v4.33) ---")
    all_bodies_data = []
    try:
        scene = Window.ActiveWindow.Scene
        bodies = list(scene.GetDescendants[IDesignBody]())
    except:
        bodies = list(GetRootPart().GetDescendants[IDesignBody]())
        
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            original_name = body.Name
            unique_name = "AUTO_BODY_" + str(i)
            
            # [v4.33] 읽기 전용 바디 대응: 직접 변경 실패 시 마스터 변경 시도
            try:
                body.Name = unique_name
            except:
                try:
                    if hasattr(body, "Master") and body.Master:
                        body.Master.Name = unique_name
                    else:
                        # 마스터도 없으면 그냥 원래 이름 사용 (JSON에는 unique_name으로 기록)
                        pass
                except: pass
            
            # JSON 데이터에는 unique_name(또는 바뀐 이름)을 기록하여 제너레이터와 동기화
            actual_name = body.Name
            body_data = {"body_index": i, "body_name": actual_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            all_bodies_data.append(body_data)
            print(" - [OK] {0} -> {1}".format(original_name, actual_name))
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
