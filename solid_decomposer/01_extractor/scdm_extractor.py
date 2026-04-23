# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.79] 전역 좌표계 변환 정상화 및 Matrix 인덱서 접근
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
except Exception as e:
    print(" - [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data", "geometry_data.json")

def get_face_data(face, matrix_obj):
    f_id = face.GetHashCode()
    data = {
        "id": f_id, "type": "Unknown", "area": face.Area * 1e6, 
        "box": {"min": [0,0,0], "max": [0,0,0]}, 
        "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False
    }
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        
        # [v4.79] Matrix 인덱서 접근 방식 사용 (m[row, col])
        bbox = shape.GetBoundingBox(matrix_obj)
        mi = bbox.MinCorner
        ma = bbox.MaxCorner
        data["box"]["min"] = [round(mi.X * 1000.0, 6), round(mi.Y * 1000.0, 6), round(mi.Z * 1000.0, 6)]
        data["box"]["max"] = [round(ma.X * 1000.0, 6), round(ma.Y * 1000.0, 6), round(ma.Z * 1000.0, 6)]
        
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        r_raw = 0.0
        # 1. 면 직접 추출
        for attr in ["Radius", "Radius0", "MajorRadius"]:
            if hasattr(geom, attr):
                r_raw = getattr(geom, attr)
                if r_raw > 1e-10: break
        
        # 2. 모서리 추출
        if r_raw <= 0:
            for edge in face.Edges:
                eg = edge.Shape.Geometry
                if hasattr(eg, "Radius"): r_raw = eg.Radius; break
                if hasattr(eg, "Radius0"): r_raw = eg.Radius0; break
        
        if r_raw > 0:
            r_mm = r_raw * 1000.0 if r_raw < 0.1 else r_raw
            data["radius"] = round(r_mm, 8)
            print("   [DEBUG-FOUND] Face {0} -> R={1:.4f}mm".format(f_id, r_mm))

        if hasattr(geom, "Frame"):
            f = geom.Frame
            m = matrix_obj
            # [v4.79] M11 대신 m[0,0] 인덱서 사용
            data["axis"] = [
                round(m[0,0]*f.DirZ.X + m[0,1]*f.DirZ.Y + m[0,2]*f.DirZ.Z, 8),
                round(m[1,0]*f.DirZ.X + m[1,1]*f.DirZ.Y + m[1,2]*f.DirZ.Z, 8),
                round(m[2,0]*f.DirZ.X + m[2,1]*f.DirZ.Y + m[2,2]*f.DirZ.Z, 8)
            ]
    except Exception as e:
        print("   [DEBUG-ERR] Face {0}: {1}".format(f_id, str(e)))
    return data

def extract_geometry():
    print("--- SCDM World-Alignment Extraction (v4.79) ---")
    final_bodies_data = []
    try:
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        
        bodies_list = list(root.GetDescendants[IDesignBody]())
        if not bodies_list:
            bodies_list = list(root.Bodies)
            for comp in root.Components:
                for b in comp.Template.Bodies: bodies_list.append(b)

        print(" - Processing {0} bodies...".format(len(bodies_list)))
        
        for i, body in enumerate(bodies_list):
            b_name = getattr(body, "Name", "Body_" + str(i))
            # [v4.79] Inverse 제거! World 좌표계를 위해 TransformToMaster 직접 사용
            t_mat = Matrix.Identity
            if body.Instance: t_mat = body.TransformToMaster
            
            bdata = {"body_index": i, "body_name": b_name, "volume": body.Shape.Volume * 1e9, "faces": []}
            for face in list(body.Faces):
                bdata["faces"].append(get_face_data(face, t_mat))
            final_bodies_data.append(bdata)
            print("   [OK] {0} complete.".format(b_name))
                
    except Exception as e: print(" - [FATAL] Extraction error: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete (World Aligned).")
except Exception as e: print("\n[FATAL] " + str(e))
