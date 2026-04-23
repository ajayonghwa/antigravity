# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.50] 스페이스클레임 내부 글로벌 함수 및 클래스에 직접 접근 (가장 확실한 방법)
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
    print(" [STEP 1] API V22 Namespace Loaded")
except Exception as e:
    print(" [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix_from_obj(m):
    res = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        t = m.Translation
        res[0][3] = t.X * 1000.0; res[1][3] = t.Y * 1000.0; res[2][3] = t.Z * 1000.0
        r = m.Rotation
        res[0][0]=r.M11; res[0][1]=r.M12; res[0][2]=r.M13
        res[1][0]=r.M21; res[1][1]=r.M22; res[1][2]=r.M23
        res[2][0]=r.M31; res[2][1]=r.M32; res[2][2]=r.M33
    except: pass
    return res

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1000000.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            bbox = face.GetBoundingBox(Matrix.Identity)
            data["origin"] = [bbox.Center.X * 1000.0, bbox.Center.Y * 1000.0, bbox.Center.Z * 1000.0]
            f = geom.Frame
            data["axis"] = [
                matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z,
                matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z,
                matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            ]
            data["box"]["min"] = [bbox.Min.X * 1000.0, bbox.Min.Y * 1000.0, bbox.Min.Z * 1000.0]
            data["box"]["max"] = [bbox.Max.X * 1000.0, bbox.Max.Y * 1000.0, bbox.Max.Z * 1000.0]
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0) * 1000.0
                if str(shape.Orientation) == "Reversed": data["is_internal"] = True
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Robust Extraction (v4.50) ---")
    all_bodies_data = []
    
    # [STEP 2] Root Part 획득
    try:
        root = GetRootPart()
        print(" [STEP 2] Root Part: {0}".format(root.Name))
    except Exception as e:
        print(" [ERROR] Failed to get Root Part: " + str(e))
        return [], [], "Unknown"
    
    # [STEP 3] 바디 탐색 (3단계)
    bodies = []
    try:
        bodies = list(Window.ActiveWindow.GetAllOccurrences[IDesignBody]())
        if not bodies: 
            print(" [INFO] GetAllOccurrences found 0, trying GetDescendants...")
            bodies = list(root.GetDescendants[IDesignBody]())
        if not bodies:
            print(" [INFO] GetDescendants found 0, trying root.Bodies...")
            bodies = list(root.Bodies)
    except Exception as e:
        print(" [DEBUG] Search Error: " + str(e))
        bodies = list(root.GetDescendants[IDesignBody]())
    
    print(" [STEP 3] Found {0} bodies".format(len(bodies)))

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
        
        body_data = {"body_index": i, "body_name": actual_name, "original_name": body.Name, "volume": body.Shape.Volume * 1e9, "faces": []}
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
    print("\n[FINISH] Geometry data saved successfully.")
except Exception as e: print("\n[FATAL] " + str(e))
