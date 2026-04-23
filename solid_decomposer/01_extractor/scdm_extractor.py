# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.71] 단위 자동 보정(Auto-Scaling) 및 심층 속성 탐색
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
        
        # 1. 전역 좌표 중심점 및 바운딩 박스
        bbox = face.GetBoundingBox(matrix_obj)
        data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
        data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        r_raw = 0.0
        method = ""
        
        # [v4.71] 심층 속성 탐색 (면)
        for obj in [geom, getattr(geom, "Circle", None), getattr(geom, "Geometry", None)]:
            if obj is None: continue
            for attr in ["Radius", "Radius0", "MajorRadius"]:
                val = getattr(obj, attr, 0.0)
                if val > 1e-10: r_raw = val; method = "FACE_DEEP"; break
            if r_raw > 0: break
            
        # 심층 속성 탐색 (모서리)
        if r_raw <= 0:
            for edge in face.Edges:
                eg = edge.Shape.Geometry
                for obj in [eg, getattr(eg, "Circle", None), getattr(eg, "Curve", None)]:
                    if obj is None: continue
                    for attr in ["Radius", "Radius0"]:
                        val = getattr(obj, attr, 0.0)
                        if val > 1e-10: r_raw = val; method = "EDGE_DEEP"; break
                    if r_raw > 0: break
                if r_raw > 0: break

        # BBox 추론 (v4.70 logic)
        if r_raw <= 0:
            l_bbox = face.GetBoundingBox(Matrix.Identity)
            dims = sorted([l_bbox.Size.X, l_bbox.Size.Y, l_bbox.Size.Z], reverse=True)
            if dims[1] > 1e-10:
                if abs(dims[0] - dims[1]) / (dims[0] + 1e-11) < 0.35:
                    r_raw = (dims[0] + dims[1]) / 4.0; method = "BBOX_INFER"
                elif abs(dims[1] - dims[2]) / (dims[1] + 1e-11) < 0.35:
                    r_raw = (dims[1] + dims[2]) / 4.0; method = "BBOX_INFER_SMALL"

        if r_raw > 0:
            # [v4.71] 단위 자동 보정 (Auto-Scaling)
            # 만약 r_raw가 0.1보다 작다면 m 단위로 보고 1000을 곱함, 크다면 이미 mm로 판단
            if r_raw < 0.1: r_mm = r_raw * 1000.0
            else: r_mm = r_raw
            
            data["radius"] = round(r_mm, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            print("   [FOUND] Face {0} -> Raw={1:.6f}, Final={2:.4f}mm ({3})".format(f_id, r_raw, r_mm, method))
            
        # 축 계산
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
    print("--- SCDM Deep Probing Extraction (v4.71) ---")
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
            b_name = getattr(body, "Name", "Body_" + str(i))
            t_mat = Matrix.Identity
            if body.Instance: t_mat = body.TransformToMaster.Inverse
            
            bdata = {"body_index": i, "body_name": b_name, "volume": body.Shape.Volume * 1e9, "faces": []}
            for face in list(body.Faces):
                bdata["faces"].append(get_face_data(face, t_mat))
            final_bodies_data.append(bdata)
            print("   [OK] Body '{0}' done.".format(b_name))
                
    except Exception as e: print(" - [FATAL] Extraction error: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Deep Probing Extraction complete.")
except Exception as e: print("\n[FATAL] " + str(e))
