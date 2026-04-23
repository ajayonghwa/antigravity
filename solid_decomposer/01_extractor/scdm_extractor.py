# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.63] Component 위치 속성 대응 (Placement/Transform) 및 적응형 행렬 연산
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
except Exception as e:
    print(" - [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        bbox = face.GetBoundingBox(Matrix.Identity)
        c = bbox.Center
        gx = matrix[0][0]*c.X + matrix[0][1]*c.Y + matrix[0][2]*c.Z + matrix[0][3]/1000.0
        gy = matrix[1][0]*c.X + matrix[1][1]*c.Y + matrix[1][2]*c.Z + matrix[1][3]/1000.0
        gz = matrix[2][0]*c.X + matrix[2][1]*c.Y + matrix[2][2]*c.Z + matrix[2][3]/1000.0
        data["origin"] = [round(gx * 1000.0, 6), round(gy * 1000.0, 6), round(gz * 1000.0, 6)]
        r = 0.0
        if hasattr(geom, "Radius"): r = geom.Radius
        elif hasattr(geom, "Radius0"): r = geom.Radius0
        if r <= 0:
            for edge in face.Edges:
                if hasattr(edge.Shape.Geometry, "Radius"): r = edge.Shape.Geometry.Radius; break
        if r > 0:
            data["radius"] = round(r * 1000.0, 6)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
        if hasattr(geom, "Frame"):
            f = geom.Frame
            nz_x = matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z
            nz_y = matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z
            nz_z = matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            data["axis"] = [round(nz_x, 6), round(nz_y, 6), round(nz_z, 6)]
    except: pass
    return data

def walk_hierarchy(part, current_matrix, results):
    for body in part.Bodies:
        results.append((body, current_matrix))
    for comp in part.Components:
        # [v4.63] Adaptive Transform Discovery
        t_obj = None
        for attr in ["Placement", "Transform", "TransformToRoot"]:
            if hasattr(comp, attr):
                t_obj = getattr(comp, attr); break
        
        m_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
        if t_obj:
            try:
                # 1. Transform 객체인 경우 (Matrix + Translation 포함)
                if hasattr(t_obj, "Matrix") and hasattr(t_obj, "Translation"):
                    m = t_obj.Matrix
                    tr = t_obj.Translation
                    m_py = [[m.M11, m.M12, m.M13, tr.X*1000.0], [m.M21, m.M22, m.M23, tr.Y*1000.0], [m.M31, m.M32, m.M33, tr.Z*1000.0]]
                # 2. Matrix 자체인 경우
                elif hasattr(t_obj, "M11"):
                    m_py = [[t_obj.M11, t_obj.M12, t_obj.M13, 0.0], [t_obj.M21, t_obj.M22, t_obj.M23, 0.0], [t_obj.M31, t_obj.M32, t_obj.M33, 0.0]]
            except: pass
        walk_hierarchy(comp.Template, m_py, results)

def extract_geometry():
    print("--- SCDM Adaptive Extraction (v4.63) ---")
    all_bodies_raw = []
    try:
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        print(" - Scanning Root: " + root.Name)
        identity = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
        walk_hierarchy(root, identity, all_bodies_raw)
        
        # 방식 2 (GetDescendants) 보완
        if not all_bodies_raw:
            try:
                for b in root.GetDescendants[IDesignBody](): all_bodies_raw.append((b, identity))
            except: pass
    except: pass
    
    unique_bodies = []
    seen = set()
    for b, m in all_bodies_raw:
        h = b.GetHashCode()
        if h not in seen: unique_bodies.append((b, m)); seen.add(h)
            
    print(" - Bodies Found: {0}".format(len(unique_bodies)))
    final_data = []
    for i, (body, matrix) in enumerate(unique_bodies):
        try:
            b_name = "Unknown"
            try: b_name = body.Name
            except: pass
            vol = 0.0
            try: vol = body.Shape.Volume * 1e9
            except: pass
            bdata = {"body_index": i, "body_name": b_name, "volume": vol, "faces": []}
            for face in list(body.Faces): bdata["faces"].append(get_face_data(face, matrix))
            final_data.append(bdata)
            print("   [OK] {0}".format(b_name))
        except: pass
    return final_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Adaptive extraction completed.")
except Exception as e: print("\n[FATAL] " + str(e))
