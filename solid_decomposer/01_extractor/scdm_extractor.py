# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.60] 재귀 탐색을 통한 전 계층 바디 추출 (Assembly 대응)
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
except Exception as e:
    print(" - [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        bbox = face.GetBoundingBox(Matrix.Identity)
        data["origin"] = [round(bbox.Center.X * 1000.0, 6), round(bbox.Center.Y * 1000.0, 6), round(bbox.Center.Z * 1000.0, 6)]
        data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
        data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]
        r = 0.0
        if hasattr(geom, "Radius"): r = geom.Radius
        elif hasattr(geom, "Radius0"): r = geom.Radius0
        if r <= 0:
            for edge in face.Edges:
                if hasattr(edge.Shape.Geometry, "Radius"): r = edge.Shape.Geometry.Radius; break
        if r > 0:
            data["radius"] = round(r * 1000.0, 6)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
        if hasattr(geom, "Frame"):
            f = geom.Frame
            data["axis"] = [
                round(matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, 6),
                round(matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z, 6),
                round(matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z, 6)
            ]
    except: pass
    return data

def find_all_bodies(part, matrix, all_bodies):
    # 1. 현재 파트의 바디 추출
    for body in part.Bodies:
        all_bodies.append((body, matrix))
    
    # 2. 하위 컴포넌트 재귀 탐색
    for comp in part.Components:
        trans = comp.TransformToRoot
        new_matrix = [[trans.Matrix.M11, trans.Matrix.M12, trans.Matrix.M13, trans.Translation.X*1000.0],
                      [trans.Matrix.M21, trans.Matrix.M22, trans.Matrix.M23, trans.Translation.Y*1000.0],
                      [trans.Matrix.M31, trans.Matrix.M32, trans.Matrix.M33, trans.Translation.Z*1000.0]]
        find_all_bodies(comp.Template, new_matrix, all_bodies)

def extract_geometry():
    print("--- SCDM Deep Discovery Extraction (v4.60) ---")
    all_bodies_raw = []
    try: 
        root = GetRootPart()
        identity = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
        find_all_bodies(root, identity, all_bodies_raw)
    except Exception as re:
        print(" - [ERROR] Discovery Failed: " + str(re))
        return [], [], "mm"
    
    print(" - Found {0} bodies in hierarchy".format(len(all_bodies_raw)))
    final_data = []
    for i, (body, matrix) in enumerate(all_bodies_raw):
        b_name = "Unknown"
        try: b_name = body.Name
        except: pass
        vol = 0.0
        try: vol = body.Shape.Volume * 1e9
        except: pass
        
        bdata = {"body_index": i, "body_name": b_name, "volume": vol, "faces": []}
        for face in list(body.Faces):
            bdata["faces"].append(get_face_data(face, matrix))
        final_data.append(bdata)
        print("   [OK] Body {0}: '{1}' extracted.".format(i, b_name))
            
    return final_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete with hierarchy search.")
except Exception as e: print("\n[FATAL] " + str(e))
