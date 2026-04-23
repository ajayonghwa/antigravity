# -*- coding: utf-8 -*-
import json
import os
import clr

# [매뉴얼 15번 지침] V22~V17 역순으로 참조 추가하는 동적 초기화
def initialize_scdm_api():
    for v in range(22, 16, -1):
        try:
            ref_name = "SpaceClaim.Api.V" + str(v)
            clr.AddReference(ref_name)
            # 성공 시 해당 버전의 네임스페이스 반환
            return v
        except: continue
    return None

API_VER = initialize_scdm_api()
if API_VER:
    # 동적 임포트 (전역 네임스페이스에 풀기 - 매뉴얼 16번)
    exec("from SpaceClaim.Api.V{0} import *".format(API_VER))
    exec("from SpaceClaim.Api.V{0}.Modeler import *".format(API_VER))
    exec("from SpaceClaim.Api.V{0}.Geometry import *".format(API_VER))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix_from_obj(m):
    res = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        if hasattr(m, "Translation"):
            t = m.Translation
            res[0][3] = t.X; res[1][3] = t.Y; res[2][3] = t.Z
        if hasattr(m, "Rotation"):
            r = m.Rotation
            try:
                res[0][0]=r.M11; res[0][1]=r.M12; res[0][2]=r.M13
                res[1][0]=r.M21; res[1][1]=r.M22; res[1][2]=r.M23
                res[2][0]=r.M31; res[2][1]=r.M32; res[2][2]=r.M33
            except:
                for row in range(3):
                    for col in range(3): res[row][col] = r.GetValue(row, col)
    except: pass
    return res

def apply_mat(m, p):
    x = m[0][0]*p.X + m[0][1]*p.Y + m[0][2]*p.Z + m[0][3]
    y = m[1][0]*p.X + m[1][1]*p.Y + m[1][2]*p.Z + m[1][3]
    z = m[2][0]*p.X + m[2][1]*p.Y + m[2][2]*p.Z + m[2][3]
    return [x, y, z]

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            # 4.43: Matrix.Identity를 동적으로 가져옴
            from SpaceClaim.Api.V22.Geometry import Matrix as ScMatrix
            bbox = face.GetBoundingBox(ScMatrix.Identity)
            data["origin"] = [bbox.Center.X, bbox.Center.Y, bbox.Center.Z]
            f = geom.Frame
            data["axis"] = [
                matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z,
                matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z,
                matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            ]
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                if str(shape.Orientation) == "Reversed": data["is_internal"] = True
        bbox = face.GetBoundingBox(ScMatrix.Identity)
        data["box"]["min"] = [bbox.Min.X, bbox.Min.Y, bbox.Min.Z]
        data["box"]["max"] = [bbox.Max.X, bbox.Max.Y, bbox.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Dynamic API Extraction (v4.43) ---")
    all_bodies_data = []
    root = GetRootPart()
    try: bodies = list(Window.ActiveWindow.GetAllOccurrences[IDesignBody]())
    except: bodies = list(root.GetDescendants[IDesignBody]())
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        matrix_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        try:
            comp = body.ParentComponent if hasattr(body, "ParentComponent") else None
            if not comp and hasattr(body, "OccurrenceParent"): comp = body.OccurrenceParent
            if comp: matrix_py = get_python_matrix_from_obj(comp.TransformToRoot)
        except: pass
        
        unique_name = "AUTO_BODY_" + str(i)
        try: body.Name = unique_name
        except: pass
        
        actual_name = body.Name
        print(" - [OK] {0} (Pos: {1:.4f}, {2:.4f}, {3:.4f})".format(actual_name, matrix_py[0][3], matrix_py[1][3], matrix_py[2][3]))
        
        body_data = {"body_index": i, "body_name": actual_name, "original_name": body.Name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
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
