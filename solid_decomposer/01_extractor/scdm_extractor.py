# -*- coding: utf-8 -*-
import json
import os
import re

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix(m):
    # [v4.31] ToString() 파싱을 통한 가장 보수적이고 확실한 행렬 추출
    try:
        s = str(m)
        # 숫자들만 모두 추출
        nums = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", s)]
        res = [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]
        if len(nums) >= 12:
            # 3x4 또는 4x4 행렬 처리
            res[0][0] = nums[0]; res[0][1] = nums[1]; res[0][2] = nums[2]; res[0][3] = nums[3]
            res[1][0] = nums[4]; res[1][1] = nums[5]; res[1][2] = nums[6]; res[1][3] = nums[7]
            res[2][0] = nums[8]; res[2][1] = nums[9]; res[2][2] = nums[10]; res[2][3] = nums[11]
        return res
    except:
        return [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]

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
    print("--- SCDM Matrix String Parsing (v4.31) ---")
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
