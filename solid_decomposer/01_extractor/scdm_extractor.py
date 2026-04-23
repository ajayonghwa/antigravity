# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix(m):
    # [v4.36] API 속성(Translation, Rotation)을 직접 추출하여 0,0,0 쏠림 근본 해결
    res = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        # 1. 이동값(Translation) 추출
        if hasattr(m, "Translation"):
            t = m.Translation
            res[0][3] = t.X; res[1][3] = t.Y; res[2][3] = t.Z
        
        # 2. 회전값(Rotation) 추출
        if hasattr(m, "Rotation"):
            r = m.Rotation # Matrix33
            # Matrix33은 M11~M33 속성을 가집니다.
            try:
                res[0][0]=r.M11; res[0][1]=r.M12; res[0][2]=r.M13
                res[1][0]=r.M21; res[1][1]=r.M22; res[1][2]=r.M23
                res[2][0]=r.M31; res[2][1]=r.M32; res[2][2]=r.M33
            except:
                # 속성이 없으면 GetValue 시도
                for row in range(3):
                    for col in range(3):
                        try: res[row][col] = r.GetValue(row, col)
                        except: pass
    except: pass
    return res

def apply_mat(m, p):
    x = m[0][0]*p.X + m[0][1]*p.Y + m[0][2]*p.Z + m[0][3]
    y = m[1][0]*p.X + m[1][1]*p.Y + m[1][2]*p.Z + m[1][3]
    z = m[2][0]*p.X + m[2][1]*p.Y + m[2][2]*p.Z + m[2][3]
    return [x, y, z]

def get_face_data(face, matrix):
    # [v4.36] Face Id 에러 방지를 위해 getattr 사용
    f_id = getattr(face, "Id", 0)
    data = {"id": f_id, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            f = geom.Frame
            data["origin"] = apply_mat(matrix, f.Origin)
            data["axis"] = [matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z, matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z]
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                if str(shape.Orientation) == "Reversed": data["is_internal"] = True
        
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            p1 = apply_mat(matrix, r.Min); p2 = apply_mat(matrix, r.Max)
            data["box"]["min"] = [min(p1[0], p2[0]), min(p1[1], p2[1]), min(p1[2], p2[2])]
            data["box"]["max"] = [max(p1[0], p2[0]), max(p1[1], p2[1]), max(p1[2], p2[2])]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Direct Property Extraction (v4.36) ---")
    all_bodies_data = []
    root = GetRootPart()
    bodies_info = []
    identity = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    
    def get_all_occurrences(part, current_matrix):
        # 1. 현재 파트의 바디 수집
        for b in part.Bodies: bodies_info.append((b, current_matrix))
        # 2. 하위 컴포넌트 재귀 탐색
        for c in part.Components:
            m_local = get_python_matrix(c.Placement)
            # 4x4 행렬 곱셈
            next_mat = [[0.0]*4 for _ in range(4)]
            for r in range(4):
                for col in range(4):
                    for k in range(4): next_mat[r][col] += current_matrix[r][k] * m_local[k][col]
            if hasattr(c, "Template") and c.Template:
                get_all_occurrences(c.Template, next_mat)

    get_all_occurrences(root, identity)
    print(" - Collected {0} bodies".format(len(bodies_info)))

    for i, (body, matrix) in enumerate(bodies_info):
        try:
            original_name = body.Name
            unique_name = "AUTO_BODY_" + str(i)
            try: RenameInstance.Execute(Selection.Create(body), unique_name)
            except: body.Name = unique_name
            
            actual_name = body.Name
            # 로그 출력 강화 (0,0,0 탈출 확인용)
            print(" - [OK] {0} (Pos: {1:.4f}, {2:.4f}, {3:.4f})".format(actual_name, matrix[0][3], matrix[1][3], matrix[2][3]))
            
            body_data = {"body_index": i, "body_name": actual_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face, matrix)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            all_bodies_data.append(body_data)
        except Exception as e:
            print(" - [ERROR] Failed on {0}: {1}".format(body.Name, str(e)))
            
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
