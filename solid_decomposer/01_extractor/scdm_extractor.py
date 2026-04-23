# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.66] 지능형 바운딩 박스 분석 및 정밀 디버그 로깅
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

def get_face_data(face, matrix_obj):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        
        bbox = face.GetBoundingBox(matrix_obj)
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        r = 0.0
        # 방식 A: 속성 탐색
        for r_attr in ["Radius", "Radius0", "MajorRadius"]:
            if hasattr(geom, r_attr):
                val = getattr(geom, r_attr)
                if val > 1e-9: r = val; break
        
        # 방식 B: 모서리 탐색
        if r <= 0:
            for edge in face.Edges:
                eg = edge.Shape.Geometry
                for r_attr in ["Radius", "Radius0"]:
                    if hasattr(eg, r_attr):
                        val = getattr(eg, r_attr)
                        if val > 1e-9: r = val; break
                if r > 0: break

        # 방식 C: 지능형 BBox 분석 (v4.66 핵심)
        local_bbox = face.GetBoundingBox(Matrix.Identity)
        dx, dy, dz = local_bbox.Size.X, local_bbox.Size.Y, local_bbox.Size.Z
        
        if r <= 0:
            dims = sorted([dx, dy, dz], reverse=True) # 큰 순서대로 정렬
            # 가장 큰 두 변이 비슷하면 원형/원통으로 간주 (타공판 대응)
            if dims[1] > 1e-9 and abs(dims[0] - dims[1]) / dims[0] < 0.2: # 20% 오차 허용
                r = (dims[0] + dims[1]) / 4.0 # (지름1+지름2)/4 = 평균 반경
                print("   [INFER] Face {0} -> R={1:.4f}mm (BBox: {2:.2f}, {3:.2f}, {4:.2f})".format(f_id, r*1000.0, dx*1000.0, dy*1000.0, dz*1000.0))

        if r > 0:
            data["radius"] = round(r * 1000.0, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
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
    print("--- SCDM Dimension-Aware Extraction (v4.66) ---")
    final_bodies_data = []
    try:
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        if not root: return [], [], "mm"
        
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
    print("\n[FINISH] Extraction complete. BBox Inference enhanced.")
except Exception as e: print("\n[FATAL] " + str(e))
