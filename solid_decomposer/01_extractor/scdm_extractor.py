# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.75] 정점 거리 분석(Vertex-Distance)을 통한 강제 반경 추출
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
        
        # 0순위: 구멍 데이터베이스
        f_master_id = face.Master.GetHashCode() if hasattr(face, "Master") else f_id
        if f_master_id in hole_db:
            r_raw = hole_db[f_master_id]
            method = "HOLE_DB"

        # 1순위: 심층 속성 탐색 (v4.71 logic)
        if r_raw <= 0:
            for obj in [geom, getattr(geom, "Circle", None)]:
                if obj is None: continue
                val = getattr(obj, "Radius", 0.0) or getattr(obj, "Radius0", 0.0)
                if val > 1e-10: r_raw = val; method = "ATTR_DEEP"; break

        # 2순위: 정점 거리 분석 (v4.75 핵심 - 최강의 백업)
        if r_raw <= 0:
            try:
                # 면의 로컬 중심점 (마스터 기준)
                l_bbox = face.GetBoundingBox(Matrix.Identity)
                l_center = l_bbox.Center
                
                distances = []
                # 모든 모서리의 정점들 조사
                for edge in face.Edges:
                    for v in [edge.StartVertex, edge.EndVertex]:
                        if v is None: continue
                        p = v.Position
                        # 중심점과의 거리 계산 (XY평면 거리 위주로 판단 시도 가능하나 일단 3D 거리)
                        dist = math.sqrt((p.X - l_center.X)**2 + (p.Y - l_center.Y)**2 + (p.Z - l_center.Z)**2)
                        if dist > 1e-10: distances.append(dist)
                
                if len(distances) >= 2:
                    avg_d = sum(distances) / len(distances)
                    # 거리의 일관성 체크 (표준편차가 작아야 원형으로 간주)
                    variance = sum((d - avg_d)**2 for d in distances) / len(distances)
                    if math.sqrt(variance) / (avg_d + 1e-11) < 0.2: # 20% 오차 허용
                        r_raw = avg_d
                        method = "VERTEX_INFER"
            except: pass

        if r_raw > 0:
            r_mm = r_raw * 1000.0 if r_raw < 0.1 else r_raw
            data["radius"] = round(r_mm, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            print("   [{0}] Face {1} -> R={2:.4f}mm".format(method, f_id, r_mm))
            
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
    print("--- SCDM Vertex-Inference Extraction (v4.75) ---")
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
                options = IdentifyHoleOptions()
                options.MatchStandardSize = False
                target = body.Master if hasattr(body, "Master") else body
                holes = target.IdentifyHoles(options)
                for h in holes:
                    h_rad = h.HoleDiameter / 2.0
                    for h_face in h.Faces:
                        hole_db[h_face.GetHashCode()] = h_rad
            except: pass

            b_name = getattr(body, "Name", "Body_" + str(i))
            t_mat = Matrix.Identity
            if body.Instance: t_mat = body.TransformToMaster.Inverse
            
            bdata = {"body_index": i, "body_name": b_name, "volume": body.Shape.Volume * 1e9, "faces": []}
            for face in list(body.Faces):
                bdata["faces"].append(get_face_data(face, t_mat, hole_db))
            final_bodies_data.append(bdata)
            print("   [OK] Body '{0}' done.".format(b_name))
                
    except Exception as e: print(" - [FATAL] Extraction error: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete (Vertex-Inference active).")
except Exception as e: print("\n[FATAL] " + str(e))
