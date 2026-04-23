# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.44] 버전 번호를 명시하지 않는 표준 임포트 방식으로 회귀
def setup_api():
    try:
        # 버전 없이 시도 (이미 로드된 환경 대응)
        import SpaceClaim.Api as Api
        return Api
    except:
        # 실패 시 V22~V17 강제 참조 시도
        for v in [22, 21, 20, 19, 18, 17]:
            try:
                clr.AddReference("SpaceClaim.Api.V" + str(v))
                exec("import SpaceClaim.Api.V{0} as Api".format(v))
                return Api
            except: continue
    return None

API = setup_api()

# 전역 접근을 위한 매핑
def get_scdm_obj(path_str):
    try:
        parts = path_str.split('.')
        obj = API
        for p in parts: obj = getattr(obj, p)
        return obj
    except: return None

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix_from_obj(m):
    res = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        t = m.Translation
        res[0][3] = t.X; res[1][3] = t.Y; res[2][3] = t.Z
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

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            # [v4.44] Matrix.Identity를 안전하게 가져옴
            sc_mat_cls = get_scdm_obj("Geometry.Matrix")
            if sc_mat_cls:
                bbox = face.GetBoundingBox(sc_mat_cls.Identity)
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
    print("--- SCDM Safe API Extraction (v4.44) ---")
    all_bodies_data = []
    root = GetRootPart()
    try:
        try: bodies = list(Window.ActiveWindow.GetAllOccurrences[IDesignBody]())
        except: bodies = list(root.GetDescendants[IDesignBody]())
    except: bodies = []
    
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
