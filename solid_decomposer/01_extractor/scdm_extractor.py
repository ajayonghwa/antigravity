# -*- coding: utf-8 -*-
import json
import os
import re

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix(m):
    # [v4.35] 가장 안정적인 문자열 기반 파싱 (숫자 12개 또는 16개 추출)
    try:
        nums = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", str(m))]
        res = [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]
        if len(nums) >= 12:
            res[0][0]=nums[0]; res[0][1]=nums[1]; res[0][2]=nums[2]; res[0][3]=nums[3]
            res[1][0]=nums[4]; res[1][1]=nums[5]; res[1][2]=nums[6]; res[1][3]=nums[7]
            res[2][0]=nums[8]; res[2][1]=nums[9]; res[2][2]=nums[10]; res[2][3]=nums[11]
        return res
    except: return [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]

def apply_mat(m, p):
    x = m[0][0]*p.X + m[0][1]*p.Y + m[0][2]*p.Z + m[0][3]
    y = m[1][0]*p.X + m[1][1]*p.Y + m[1][2]*p.Z + m[1][3]
    z = m[2][0]*p.X + m[2][1]*p.Y + m[2][2]*p.Z + m[2][3]
    return [x, y, z]

def get_face_data(face, matrix):
    data = {"id": face.Id, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    shape = face.Shape
    if hasattr(shape, "Geometry"):
        geom = shape.Geometry
        g_type = geom.GetType().Name
        data["type"] = g_type
        f = geom.Frame
        data["origin"] = apply_mat(matrix, f.Origin)
        # 벡터(방향)는 평행이동 제외
        data["axis"] = [matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z, matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z]
        if "Cylinder" in g_type or "Conical" in g_type:
            data["radius"] = getattr(geom, "Radius", 0.0)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
    r = getattr(shape, "Range", face.Box)
    p1 = apply_mat(matrix, r.Min); p2 = apply_mat(matrix, r.Max)
    data["box"]["min"] = [min(p1[0], p2[0]), min(p1[1], p2[1]), min(p1[2], p2[2])]
    data["box"]["max"] = [max(p1[0], p2[0]), max(p1[1], p2[1]), max(p1[2], p2[2])]
    return data

def extract_geometry():
    print("--- SCDM Hybrid Matrix Extraction (v4.35) ---")
    all_bodies_data = []
    root = GetRootPart()
    bodies_info = []
    identity = [[1.0,0,0,0], [0,1.0,0,0], [0,0,1.0,0], [0,0,0,1.0]]
    
    def get_all_occurrences(part, current_matrix):
        for b in part.Bodies: bodies_info.append((b, current_matrix))
        for c in part.Components:
            m_local = get_python_matrix(c.Placement)
            # 4x4 MatMul
            next_mat = [[0.0]*4 for _ in range(4)]
            for r in range(4):
                for col in range(4):
                    for k in range(4): next_mat[r][col] += current_matrix[r][k] * m_local[k][col]
            get_all_occurrences(c.Template, next_mat)

    get_all_occurrences(root, identity)
    print(" - Collected {0} bodies".format(len(bodies_info)))

    for i, (body, matrix) in enumerate(bodies_info):
        original_name = body.Name
        unique_name = "AUTO_BODY_" + str(i)
        try: RenameInstance.Execute(Selection.Create(body), unique_name)
        except: body.Name = unique_name
        
        actual_name = body.Name
        print(" - [OK] Processing {0} (Matrix T: {1:.3f}, {2:.3f}, {3:.3f})".format(actual_name, matrix[0][3], matrix[1][3], matrix[2][3]))
        
        body_data = {"body_index": i, "body_name": actual_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
        for j, face in enumerate(list(body.Faces)):
            fdata = get_face_data(face, matrix)
            fdata["index"] = j
            body_data["faces"].append(fdata)
        all_bodies_data.append(body_data)
            
    unit_str = str(root.Document.Units.Length.Symbol)
    return all_bodies_data, [], unit_str

results, warns, uinfo = extract_geometry()
final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
print("\n[FINISH] Geometry data saved.")
