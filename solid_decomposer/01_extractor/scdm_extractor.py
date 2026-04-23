# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [v4.68] 전천후 반경 추출 (Any-Two BBox Match + Area/Height 역산)
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
        
        # 1. 전역 좌표 중심점
        bbox = face.GetBoundingBox(matrix_obj)
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        r = 0.0
        method = ""
        # 방식 A: API 속성 직접 탐색
        for r_attr in ["Radius", "Radius0", "MajorRadius"]:
            if hasattr(geom, r_attr):
                val = getattr(geom, r_attr)
                if val > 1e-7: r = val; method = "API_ATTR"; break
        
        # 방식 B: 모서리(Edge) 전수 조사
        if r <= 0:
            for edge in face.Edges:
                eg = edge.Shape.Geometry
                for r_attr in ["Radius", "Radius0"]:
                    if hasattr(eg, r_attr):
                        val = getattr(eg, r_attr)
                        if val > 1e-7: r = val; method = "EDGE_GEOM"; break
                if r > 0: break

        # 방식 C & D: 기하학적 추론 (v4.68 핵심)
        local_bbox = face.GetBoundingBox(Matrix.Identity)
        dx, dy, dz = local_bbox.Size.X, local_bbox.Size.Y, local_bbox.Size.Z
        dims = sorted([dx, dy, dz], reverse=True) # [Max, Mid, Min]
        
        if r <= 0 and dims[1] > 1e-7:
            # 방식 C: 어떤 두 변이라도 비슷하면 원형/원통으로 간주
            # (Case 1: Max-Mid 비슷 -> 납작한 원반 / Case 2: Mid-Min 비슷 -> 길쭉한 원통)
            if abs(dims[0] - dims[1]) / dims[0] < 0.2:
                r = (dims[0] + dims[1]) / 4.0
                method = "BBOX_MAX_MID"
            elif abs(dims[1] - dims[2]) / (dims[1] + 1e-9) < 0.2:
                r = (dims[1] + dims[2]) / 4.0
                method = "BBOX_MID_MIN"
            
            # 방식 D: 넓이와 최대 높이를 이용한 역산 (Area = 2*pi*r*h)
            if r <= 0 and dims[0] > 1e-7:
                # r = Area / (2 * pi * h)
                r_calc = (face.Area) / (2 * math.pi * dims[0])
                if r_calc > 1e-7 and r_calc < dims[0]: # 계산된 반경이 유효한 범위 내일 때
                    r = r_calc
                    method = "AREA_INFER"

        if r > 0:
            data["radius"] = round(r * 1000.0, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            print("   [FOUND] Face {0} -> R={1:.4f}mm (Method: {2})".format(f_id, r*1000.0, method))
            
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
    print("--- SCDM Universal Extraction (v4.68) ---")
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

        print(" - Processing {0} body occurrences...".format(len(all_bodies)))
        
        for i, body in enumerate(all_bodies):
            b_name = getattr(body, "Name", "Body_" + str(i))
            t_mat = Matrix.Identity
            if body.Instance: t_mat = body.TransformToMaster.Inverse
            
            bdata = {"body_index": i, "body_name": b_name, "volume": body.Shape.Volume * 1e9, "faces": []}
            for face in list(body.Faces):
                bdata["faces"].append(get_face_data(face, t_mat))
            final_bodies_data.append(bdata)
            print("   [OK] Body '{0}' extraction complete.".format(b_name))
                
    except Exception as e: print(" - [FATAL] Extraction error: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Universal extraction complete.")
except Exception as e: print("\n[FATAL] " + str(e))
