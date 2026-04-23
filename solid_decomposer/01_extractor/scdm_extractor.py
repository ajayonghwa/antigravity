# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.73] MatchStandardSize=False 설정을 통한 모든 구멍 식별
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

def get_face_data(face, matrix_obj, hole_db):
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
        
        bbox = face.GetBoundingBox(matrix_obj)
        data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
        data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        r_raw = 0.0
        method = ""
        
        # 0순위: 구멍 데이터베이스 (v4.73 핵심)
        if f_id in hole_db:
            r_raw = hole_db[f_id]
            method = "HOLE_DB"

        # 1순위: 모서리 탐색
        if r_raw <= 0:
            for edge in face.Edges:
                eg = edge.Shape.Geometry
                for attr in ["Radius", "Radius0"]:
                    val = getattr(eg, attr, 0.0)
                    if val > 1e-10: r_raw = val; method = "EDGE_DEEP"; break
                if r_raw > 0: break

        # 2순위: 면 탐색
        if r_raw <= 0:
            for attr in ["Radius", "Radius0", "MajorRadius"]:
                val = getattr(geom, attr, 0.0)
                if val > 1e-10: r_raw = val; method = "FACE_DEEP"; break

        # 3순위: BBox 추론
        if r_raw <= 0:
            l_bbox = face.GetBoundingBox(Matrix.Identity)
            dims = sorted([l_bbox.Size.X, l_bbox.Size.Y, l_bbox.Size.Z], reverse=True)
            if dims[1] > 1e-10:
                if abs(dims[0] - dims[1]) / (dims[0] + 1e-11) < 0.35:
                    r_raw = (dims[0] + dims[1]) / 4.0; method = "BBOX_INFER"
                elif abs(dims[1] - dims[2]) / (dims[1] + 1e-11) < 0.35:
                    r_raw = (dims[1] + dims[2]) / 4.0; method = "BBOX_INFER_SMALL"

        if r_raw > 0:
            r_mm = r_raw * 1000.0 if r_raw < 0.1 else r_raw
            data["radius"] = round(r_mm, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            if method == "HOLE_DB":
                print("   [HOLE] Face {0} (R={1:.4f}mm)".format(f_id, r_mm))
            else:
                print("   [FOUND] Face {0} (R={1:.4f}mm via {2})".format(f_id, r_mm, method))
            
        if hasattr(geom, "Frame"):
            f = geom.Frame
            m = matrix_obj
            data["axis"] = [
                round(m.M11*f.DirZ.X + m.M12*f.DirZ.Y + m.M13*f.DirZ.Z, 8),
                round(m.M21*f.DirZ.X + m.M22*f.DirZ.Y + m.M23*f.DirZ.Z, 8),
                round(m.M31*f.DirZ.X + m.M32*f.DirZ.Y + m.M33*f.DirZ.Z, 8)
            ]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Global Hole Extraction (v4.73) ---")
    final_bodies_data = []
    try:
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        
        all_bodies = list(root.GetDescendants[IDesignBody]())
        if not all_bodies:
            all_bodies = list(root.Bodies)
            for comp in root.Components:
                for b in comp.Template.Bodies: all_bodies.append(b)

        print(" - Processing {0} bodies...".format(len(all_bodies)))
        
        for i, body in enumerate(all_bodies):
            hole_db = {}
            try:
                # [v4.73] 모든 구멍(비표준 포함) 식별 옵션 적용
                options = IdentifyHoleOptions()
                options.MatchStandardSize = False
                
                holes = body.IdentifyHoles(options)
                print("   [HOLE-DATABASE] Found {0} total holes in body {1}".format(len(holes), i))
                for h in holes:
                    h_rad = h.HoleDiameter / 2.0
                    for h_face in h.Faces:
                        hole_db[h_face.GetHashCode()] = h_rad
            except Exception as he:
                print("   [WARN] IdentifyHoles failed: " + str(he))

            b_name = getattr(body, "Name", "Body_" + str(i))
            t_mat = Matrix.Identity
            if body.Instance: t_mat = body.TransformToMaster.Inverse
            
            bdata = {"body_index": i, "body_name": b_name, "volume": body.Shape.Volume * 1e9, "faces": []}
            for face in list(body.Faces):
                bdata["faces"].append(get_face_data(face, t_mat, hole_db))
            final_bodies_data.append(bdata)
            print("   [OK] Body '{0}' extraction complete.".format(b_name))
                
    except Exception as e: print(" - [FATAL] Extraction error: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Universal extraction complete (MatchStandardSize=False).")
except Exception as e: print("\n[FATAL] " + str(e))
