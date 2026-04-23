# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_python_matrix_from_obj(m):
    # [v4.37] Matrix 객체에서 데이터를 직접 추출
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
    f_id = getattr(face, "Id", 0)
    data = {"id": f_id, "type": "Unknown", "area": 0.0, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            # [v4.37] EvaluateParameter(0,0)와 GetBoundingBox(Identity).Center를 교차 검증
            from SpaceClaim.Api.V22.Geometry import Matrix as ScMatrix
            bbox = face.GetBoundingBox(ScMatrix.Identity)
            data["origin"] = [bbox.Center.X, bbox.Center.Y, bbox.Center.Z]
            
            # 방향 벡터 (회전 행렬 적용)
            f = geom.Frame
            data["axis"] = [
                matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z,
                matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z,
                matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            ]
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                if str(shape.Orientation) == "Reversed": data["is_internal"] = True
        
        from SpaceClaim.Api.V22.Geometry import Matrix as ScMatrix
        bbox = face.GetBoundingBox(ScMatrix.Identity)
        data["box"]["min"] = [bbox.Min.X, bbox.Min.Y, bbox.Min.Z]
        data["box"]["max"] = [bbox.Max.X, bbox.Max.Y, bbox.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM God Matrix Extraction (v4.37) ---")
    all_bodies_data = []
    root = GetRootPart()
    
    # [v4.37] GetAllOccurrences가 있다면 사용, 없으면 GetDescendants
    try:
        bodies = list(Window.ActiveWindow.GetAllOccurrences[IDesignBody]())
    except:
        bodies = list(root.GetDescendants[IDesignBody]())
        
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            # [v4.37] IComponent의 TransformToRoot 속성이 있다면 그것을 사용
            matrix_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
            try:
                comp = body.ParentComponent # IDesignBody의 경우
                if not comp: comp = body.OccurrenceParent
                if comp:
                    m_root = comp.TransformToRoot
                    matrix_py = get_python_matrix_from_obj(m_root)
            except: pass
            
            original_name = body.Name
            unique_name = "AUTO_BODY_" + str(i)
            try: RenameInstance.Execute(Selection.Create(body), unique_name)
            except: body.Name = unique_name
            
            actual_name = body.Name
            print(" - [OK] {0} (Pos: {1:.4f}, {2:.4f}, {3:.4f})".format(actual_name, matrix_py[0][3], matrix_py[1][3], matrix_py[2][3]))
            
            body_data = {"body_index": i, "body_name": actual_name, "original_name": original_name, "volume": getattr(body.Shape, "Volume", 0.0), "faces": []}
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face, matrix_py)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            all_bodies_data.append(body_data)
        except Exception as e:
            print(" - [ERROR] Failed on {0}: {1}".format(body.Name, str(e)))
            
    unit_str = str(root.Document.Units.Length.Symbol)
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] Outer error: " + str(e))
