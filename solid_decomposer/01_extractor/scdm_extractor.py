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
    data = {"id": 0, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}}
    try:
        if hasattr(face, "Id"): data["id"] = face.Id
        shape = face.Shape if hasattr(face, "Shape") else face
        data["area"] = shape.Area if hasattr(shape, "Area") else 0.0
        
        # Bounding Box (Fallback용)
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]

        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            # [v4.5] Evaluation 엔진을 사용한 정밀 좌표 추출 (World 기준)
            try:
                eval = face.GetEvaluation()
                # 면의 중앙 파라미터에서 위치와 법선/축 추출
                mid_uv = eval.ParamRange.Mid
                pos = eval.Evaluate(mid_uv)
                data["origin"] = [pos.Point.X, pos.Point.Y, pos.Point.Z]
                
                if "Cylinder" in g_type or "Conical" in g_type:
                    data["radius"] = geom.Radius
                    # 실린더의 경우 축 방향(Direction)이 중요
                    frame = geom.Frame
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    # 원점은 축 위의 한 점으로 재설정 (더 안정적)
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                    
                    data["is_internal"] = False
                    if hasattr(shape, "Orientation"):
                        if str(shape.Orientation) == "Reversed": data["is_internal"] = True
                elif "Plane" in g_type:
                    data["normal"] = [pos.Normal.X, pos.Normal.Y, pos.Normal.Z]
            except: pass
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Precision Extraction (v4.5) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    def collect(part, blist):
        for b in part.Bodies: blist.append(b)
        for c in part.Components:
            if c.Template: collect(c.Template, blist)
    
    bodies = []
    collect(root, bodies)

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
            for j, face in enumerate(face_list):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
                fmap[face] = j
            
            # 인접성
            for e in body.Edges:
                if e.Faces.Count == 2:
                    idx1, idx2 = fmap.get(e.Faces[0]), fmap.get(e.Faces[1])
                    if idx1 is not None and idx2 is not None:
                        body_data["adjacency"].append([idx1, idx2])

            all_bodies_data.append(body_data)
            print(" - [OK] {0}".format(uname))
        except: pass
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("[FINISH] Data saved.")
except Exception as e: print("[FATAL] " + str(e))
