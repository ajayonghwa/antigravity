# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix(m):
    try:
        res = [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]
        try: res[0][0] = m.M11; res[0][1] = m.M12; res[0][2] = m.M13; res[0][3] = m.M14
        except: pass
        try: res[1][0] = m.M21; res[1][1] = m.M22; res[1][2] = m.M23; res[1][3] = m.M24
        except: pass
        try: res[2][0] = m.M31; res[2][1] = m.M32; res[2][2] = m.M33; res[2][3] = m.M34
        except: pass
        if res[0][0] == 1.0 and res[0][3] == 0:
            try:
                for r in range(3):
                    for c in range(4): res[r][c] = m.GetValue(r, c)
            except: pass
        return res
    except: return [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]

def apply_mat(m, p):
    x = m[0][0]*p.X + m[0][1]*p.Y + m[0][2]*p.Z + m[0][3]
    y = m[1][0]*p.X + m[1][1]*p.Y + m[1][2]*p.Z + m[1][3]
    z = m[2][0]*p.X + m[2][1]*p.Y + m[2][2]*p.Z + m[2][3]
    return [x, y, z]

def get_face_data(face, matrix):
    data = {"id": 0, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        if hasattr(face, "Id"): data["id"] = face.Id
        shape = face.Shape if hasattr(face, "Shape") else face
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            f = geom.Frame
            data["origin"] = apply_mat(matrix, f.Origin)
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                data["axis"] = [matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z, matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z]
                if hasattr(shape, "Orientation") and str(shape.Orientation) == "Reversed": data["is_internal"] = True
            elif "Plane" in g_type:
                data["normal"] = [matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z, matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z]
        r = getattr(shape, "Range", getattr(face, "Box", getattr(face, "BoundingBox", None)))
        if r:
            p1 = apply_mat(matrix, r.Min); p2 = apply_mat(matrix, r.Max)
            data["box"]["min"] = [min(p1[0], p2[0]), min(p1[1], p2[1]), min(p1[2], p2[2])]; data["box"]["max"] = [max(p1[0], p2[0]), max(p1[1], p2[1]), max(p1[2], p2[2])]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Unique ID Extraction (v4.29) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    bodies_info = []
    identity = [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]
    def get_all_occurrences(part, current_matrix):
        for b in part.Bodies: bodies_info.append((b, current_matrix))
        for c in part.Components:
            try:
                m_local = get_python_matrix(c.Placement)
                next_matrix = [[0.0]*4 for _ in range(4)]
                for r in range(4):
                    for c_idx in range(4):
                        for k in range(4): next_matrix[r][c_idx] += current_matrix[r][k] * m_local[k][c_idx]
            except: next_matrix = current_matrix
            if hasattr(c, "Template") and c.Template: get_all_occurrences(c.Template, next_matrix)
    get_all_occurrences(root, identity)
    
    # [v4.29] 바디 이름 고유화 강제 적용 (AUTO_BODY_0 ...)
    for i, (body, matrix) in enumerate(bodies_info):
        try:
            original_name = body.Name
            unique_name = "AUTO_BODY_" + str(i)
            body.Name = unique_name
            body_data = {"body_index": i, "body_name": unique_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face, matrix)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            all_bodies_data.append(body_data)
            print(" - [RENAME] {0} -> {1}".format(original_name, unique_name))
        except Exception as e: print(" - [ERROR] " + str(e))
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] Outer error: " + str(e))
