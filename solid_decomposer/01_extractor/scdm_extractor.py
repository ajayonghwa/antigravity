# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.48] 이름 충돌 방지를 위해 네임스페이스를 별칭으로 관리
try:
    clr.AddReference("SpaceClaim.Api.V22")
    import SpaceClaim.Api.V22 as SCDM
    import SpaceClaim.Api.V22.Modeler as Modeler
    import SpaceClaim.Api.V22.Geometry as Geometry
    import SpaceClaim.Api.V22.Scripting as Scripting
    import SpaceClaim.Api.V22.Commands as Commands
    print(" - [INFO] API V22 Absolute Mapping Success")
except Exception as e:
    print(" - [ERROR] API Mapping Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix_from_obj(m):
    res = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        t = m.Translation
        res[0][3] = t.X; res[1][3] = t.Y; res[2][3] = t.Z
        r = m.Rotation
        res[0][0]=r.M11; res[0][1]=r.M12; res[0][2]=r.M13
        res[1][0]=r.M21; res[1][1]=r.M22; res[1][2]=r.M23
        res[2][0]=r.M31; res[2][1]=r.M32; res[2][2]=r.M33
    except: pass
    return res

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            # v4.48: 절대 경로 사용
            bbox = face.GetBoundingBox(Geometry.Matrix.Identity)
            data["origin"] = [bbox.Center.X, bbox.Center.Y, bbox.Center.Z]
            f = geom.Frame
            data["axis"] = [
                matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z,
                matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z,
                matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            ]
            data["box"]["min"] = [bbox.Min.X, bbox.Min.Y, bbox.Min.Z]
            data["box"]["max"] = [bbox.Max.X, bbox.Max.Y, bbox.Max.Z]
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                if str(shape.Orientation) == "Reversed": data["is_internal"] = True
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Absolute Extraction (v4.48) ---")
    all_bodies_data = []
    root = SCDM.PartExtensions.GetRootPart(SCDM.Window.ActiveWindow.Document) # 안전한 Root 획득
    try:
        bodies = list(SCDM.Window.ActiveWindow.GetAllOccurrences[SCDM.IDesignBody]())
        if not bodies: bodies = list(root.GetDescendants[SCDM.IDesignBody]())
    except:
        bodies = list(root.GetDescendants[SCDM.IDesignBody]())
    
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        matrix_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        try:
            comp = body.ParentComponent
            if not comp: comp = body.OccurrenceParent
            if comp: matrix_py = get_python_matrix_from_obj(comp.TransformToRoot)
        except: pass
        
        unique_name = "AUTO_BODY_" + str(i)
        try: body.Name = unique_name
        except: pass
        
        actual_name = body.Name
        print(" - [OK] {0} (Pos: {1:.4f}, {2:.4f}, {3:.4f})".format(actual_name, matrix_py[0][3], matrix_py[1][3], matrix_py[2][3]))
        
        body_data = {"body_index": i, "body_name": actual_name, "original_name": body.Name, "volume": body.Shape.Volume, "faces": []}
        for j, face in enumerate(list(body.Faces)):
            try:
                fdata = get_face_data(face, matrix_py)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            except: pass
        all_bodies_data.append(body_data)
            
    unit_str = str(root.Document.Units.Length.Symbol)
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] " + str(e))
