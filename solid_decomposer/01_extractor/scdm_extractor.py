# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.64] IDocObject.TransformToMaster.Inverse를 활용한 정석적인 변환 로직
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
        
        # 1. 루트 기준 바운딩 박스 추출 (API Matrix 객체 직접 사용)
        bbox = face.GetBoundingBox(matrix_obj)
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 6), round(c.Y * 1000.0, 6), round(c.Z * 1000.0, 6)]
        
        # 2. 반경 추출 (Edge 기반 Fallback 포함)
        r = 0.0
        if hasattr(geom, "Radius"): r = geom.Radius
        elif hasattr(geom, "Radius0"): r = geom.Radius0
        if r <= 0:
            for edge in face.Edges:
                if hasattr(edge.Shape.Geometry, "Radius"): r = edge.Shape.Geometry.Radius; break
        
        if r > 0:
            data["radius"] = round(r * 1000.0, 6)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
        # 3. 축(Axis) 계산 (Matrix 회전 성분 적용)
        if hasattr(geom, "Frame"):
            f = geom.Frame
            m = matrix_obj
            nz_x = m.M11*f.DirZ.X + m.M12*f.DirZ.Y + m.M13*f.DirZ.Z
            nz_y = m.M21*f.DirZ.X + m.M22*f.DirZ.Y + m.M23*f.DirZ.Z
            nz_z = m.M31*f.DirZ.X + m.M32*f.DirZ.Y + m.M33*f.DirZ.Z
            data["axis"] = [round(nz_x, 6), round(nz_y, 6), round(nz_z, 6)]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Occurrence-Based Extraction (v4.64) ---")
    final_bodies_data = []
    try:
        root = GetRootPart()
        if not root:
            try: root = Application.GetActiveDocument().MainPart
            except: pass
        if not root: return [], [], "mm"
        
        print(" - Active Root: " + root.Name)
        
        # 모든 디자인 바디 오커런스 추출 (계층 구조 자동 포함)
        all_bodies = list(root.GetDescendants[IDesignBody]())
        if not all_bodies:
            print(" - [WARN] No bodies found via GetDescendants. Trying manual fallback...")
            all_bodies = list(root.Bodies)
            for comp in root.Components:
                for b in comp.Template.Bodies: all_bodies.append(b)

        print(" - Total occurrences identified: {0}".format(len(all_bodies)))
        
        for i, body in enumerate(all_bodies):
            try:
                b_name = "Body_" + str(i)
                try: b_name = body.Name
                except: pass
                
                # [v4.64] 오커런스 변환의 정석: TransformToMaster.Inverse
                # root에서 body로 가는 변환 행렬을 즉시 얻음
                total_matrix = Matrix.Identity
                if body.Instance:
                    total_matrix = body.TransformToMaster.Inverse
                
                vol = 0.0
                try: vol = body.Shape.Volume * 1e9
                except: pass
                
                bdata = {"body_index": i, "body_name": b_name, "volume": vol, "faces": []}
                for face in list(body.Faces):
                    bdata["faces"].append(get_face_data(face, total_matrix))
                
                final_bodies_data.append(bdata)
                print("   [OK] {0} extracted successfully.".format(b_name))
            except Exception as be:
                print("   [SKIP] Error in body {0}: {1}".format(i, str(be)))
                
    except Exception as e:
        print(" - [FATAL] Extraction Loop Failed: " + str(e))
            
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete using Occurrence Transforms.")
except Exception as e: print("\n[FATAL] " + str(e))
