# -*- coding: utf-8 -*-
import json
import os
import clr
import math

def load_scdm_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        import SpaceClaim.Api.V22 as scapi
        return scapi
    except: return None

scapi = load_scdm_api()

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face):
    data = {
        "id": 0, "type": "Unknown", "area": 0.0, 
        "box": {"min": [0,0,0], "max": [0,0,0]},
        "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False
    }
    try:
        if hasattr(face, "Id"): data["id"] = face.Id
        shape = face.Shape if hasattr(face, "Shape") else face
        data["area"] = shape.Area if hasattr(shape, "Area") else 0.0
        
        # [v4.6] 1순위: 기본 지오메트리 정보 (절대 누락 금지)
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                if hasattr(geom, "Frame"):
                    f = geom.Frame
                    data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                    data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                
                # 내경 판별
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                if hasattr(geom, "Frame"):
                    f = geom.Frame
                    data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                    data["normal"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]

        # [v4.6] 2순위: 정밀 평가 엔진 시도 (보정용)
        try:
            eval = face.GetEvaluation()
            pos = eval.Evaluate(eval.ParamRange.Mid)
            # 기본 원점이 0,0,0인 경우에만 평가값으로 보정
            if data["origin"] == [0,0,0]:
                data["origin"] = [pos.Point.X, pos.Point.Y, pos.Point.Z]
        except: pass

        # Bounding Box
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Robust Extraction Engine (v4.6) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass
    print(" - Units: {0}".format(unit_str))

    def collect(part, blist):
        for b in part.Bodies: blist.append(b)
        for c in part.Components:
            if c.Template: collect(c.Template, blist)
    
    bodies = []
    collect(root, bodies)
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            bname = body.Name
            uname = "AUTO_BODY_" + str(i)
            body.Name = uname
            
            body_data = {
                "body_index": i, "body_name": uname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": [], "adjacency": []
            }

            face_list = list(body.Faces)
            fmap = {}
            cyl_count = 0
            for j, face in enumerate(face_list):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
                fmap[face] = j
                if "Cylinder" in fdata["type"]: cyl_count += 1
            
            all_bodies_data.append(body_data)
            print(" - [OK] {0}: {1} faces (Cylinders: {2})".format(uname, len(face_list), cyl_count))
        except Exception as e:
            print(" - [ERROR] Failed to process {0}: {1}".format(body.Name, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved successfully.")
except Exception as e: print("\n[FATAL] " + str(e))
