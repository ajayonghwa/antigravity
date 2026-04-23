# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.69] 객체 속성 조사(dir) 및 안정 버전 로직 복구
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
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        
        # 전역 중심점 계산
        bbox = face.GetBoundingBox(matrix_obj)
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        r = 0.0
        method = ""
        
        # [v4.69 DEBUG] 기하 객체 속성 조사 (최초 1회성 로깅)
        # attrs = dir(geom)
        # if "Cylinder" in data["type"]: print("   [DEBUG] Cylinder Attrs: " + str(attrs[:10]))

        # 1순위: 모서리(Edge) 기하 정보 (안정 버전에서 주로 쓰던 방식)
        for edge in face.Edges:
            e_geom = edge.Shape.Geometry
            # ICircle 또는 직접 속성 체크
            for r_attr in ["Radius", "Radius0"]:
                if hasattr(e_geom, r_attr):
                    val = getattr(e_geom, r_attr)
                    if val > 1e-8: r = val; method = "EDGE_GEOM"; break
            if r > 0: break
            
        # 2순위: 면(Face) 기하 정보
        if r <= 0:
            for r_attr in ["Radius", "Radius0", "MajorRadius"]:
                if hasattr(geom, r_attr):
                    val = getattr(geom, r_attr)
                    if val > 1e-8: r = val; method = "FACE_GEOM"; break

        # 3순위: 바운딩 박스 추론 (최후의 수단)
        if r <= 0:
            l_bbox = face.GetBoundingBox(Matrix.Identity)
            dx, dy, dz = l_bbox.Size.X, l_bbox.Size.Y, l_bbox.Size.Z
            dims = sorted([dx, dy, dz], reverse=True)
            if dims[1] > 1e-8:
                # 어느 두 변이 대략적으로 비슷하면 (오차 30%까지 허용)
                if abs(dims[0] - dims[1]) / (dims[0] + 1e-9) < 0.3:
                    r = (dims[0] + dims[1]) / 4.0
                    method = "BBOX_INFER"
                elif abs(dims[1] - dims[2]) / (dims[1] + 1e-9) < 0.3:
                    r = (dims[1] + dims[2]) / 4.0
                    method = "BBOX_INFER_SMALL"

        if r > 0:
            data["radius"] = round(r * 1000.0, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            print("   [FOUND] Face {0} ({1}) -> R={2:.4f}mm via {3}".format(f_id, data["type"], r*1000.0, method))
            
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
    print("--- SCDM Legacy Recovery Extraction (v4.69) ---")
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
            print("   [OK] {0} complete.".format(b_name))
                
    except Exception as e: print(" - [FATAL] Extraction error: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete. Legacy paths recovered.")
except Exception as e: print("\n[FATAL] " + str(e))
