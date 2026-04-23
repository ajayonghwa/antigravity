# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.54] 매뉴얼 기반 안전성 강화 및 mm 단위 보정
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
    print(" - [STEP 1] API V22 Standard Load")
except Exception as e:
    print(" - [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix_from_obj(m):
    res = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        t = m.Translation
        res[0][3] = round(t.X * 1000.0, 6)
        res[1][3] = round(t.Y * 1000.0, 6)
        res[2][3] = round(t.Z * 1000.0, 6)
        r = m.Rotation
        res[0][0]=r.M11; res[0][1]=r.M12; res[0][2]=r.M13
        res[1][0]=r.M21; res[1][1]=r.M22; res[1][2]=r.M23
        res[2][0]=r.M31; res[2][1]=r.M32; res[2][2]=r.M33
    except: pass
    return res

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            bbox = face.GetBoundingBox(Matrix.Identity)
            data["origin"] = [round(bbox.Center.X * 1000.0, 6), round(bbox.Center.Y * 1000.0, 6), round(bbox.Center.Z * 1000.0, 6)]
            f = geom.Frame
            data["axis"] = [
                matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z,
                matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z,
                matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            ]
            data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
            data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = round(getattr(geom, "Radius", 0.0) * 1000.0, 6)
                if str(shape.Orientation) == "Reversed": data["is_internal"] = True
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Standard Extraction (v4.54) ---")
    all_bodies_data = []
    
    try: root = GetRootPart()
    except: return [], [], "mm"
    
    bodies = []
    try:
        bodies = list(root.GetDescendants[IDesignBody]())
        if not bodies: bodies = list(root.Bodies)
    except: bodies = list(root.Bodies)
    
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        matrix_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        try:
            comp = getattr(body, "ParentComponent", None)
            if not comp: comp = getattr(body, "OccurrenceParent", None)
            if comp: matrix_py = get_python_matrix_from_obj(comp.TransformToRoot)
        except: pass
        
        unique_name = "AUTO_BODY_" + str(i)
        try: body.Name = unique_name
        except: pass
        
        actual_name = body.Name
        print(" - [OK] {0} (Pos: {1:.2f}, {2:.2f}, {3:.2f} mm)".format(actual_name, matrix_py[0][3], matrix_py[1][3], matrix_py[2][3]))
        
        # 매뉴얼 21803행에 따라 Shape 존재 여부 확인 후 Volume 계산
        vol = 0.0
        try:
            shape = getattr(body, "Shape", None)
            if shape: vol = shape.Volume * 1e9
        except: pass
        
        body_data = {"body_index": i, "body_name": actual_name, "original_name": body.Name, "volume": vol, "faces": []}
        for j, face in enumerate(list(body.Faces)):
            try:
                fdata = get_face_data(face, matrix_py)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            except: pass
        all_bodies_data.append(body_data)
            
    return all_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete.")
except Exception as e: print("\n[FATAL] " + str(e))
