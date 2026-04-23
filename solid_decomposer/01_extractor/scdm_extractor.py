# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.78] Box 객체의 MinCorner/MaxCorner를 통한 좌표 추출 오류 해결
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
        
        # [v4.78] Modeler.Box는 MinCorner, MaxCorner 속성을 가짐
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
            print("   [DEBUG-FOUND] Face {0} ({1}) -> Raw={2:.6f}, R={3:.4f}mm".format(f_id, data["type"], r_raw, r_mm))

        if hasattr(geom, "Frame"):
            f = geom.Frame
            m = matrix_obj
            data["axis"] = [
                round(m.M11*f.DirZ.X + m.M12*f.DirZ.Y + m.M13*f.DirZ.Z, 8),
                round(m.M21*f.DirZ.X + m.M22*f.DirZ.Y + m.M23*f.DirZ.Z, 8),
                round(m.M31*f.DirZ.X + m.M32*f.DirZ.Y + m.M33*f.DirZ.Z, 8)
            ]
    except Exception as e:
        print("   [DEBUG-ERR] Face {0}: {1}".format(f_id, str(e)))
    return data

def extract_geometry():
    print("--- SCDM Box Compatibility Extraction (v4.78) ---")
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
            t_mat = Matrix.Identity
            if body.Instance: t_mat = body.TransformToMaster.Inverse
            
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
    print("\n[FINISH] Extraction complete (v4.78 Box Corners fixed).")
except Exception as e: print("\n[FATAL] " + str(e))
