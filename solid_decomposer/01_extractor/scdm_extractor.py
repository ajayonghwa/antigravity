# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.62] 문서 계층 재귀 탐색 및 정밀 행렬 연산 (Window 방식 제외)
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
        
        # 행렬 정보를 이용한 루트 기준 바운딩 박스 추출
        # (v4.62) Matrix.Create 사용 대신 수동 변환 적용의 정확성 확보
        bbox = face.GetBoundingBox(Matrix.Identity)
        center = bbox.Center
        
        # 전역 좌표 변환 (Matrix * Vector)
        # matrix = [ [m11, m12, m13, tx], [m21, m22, m23, ty], [m31, m32, m33, tz] ]
        gx = matrix[0][0]*center.X + matrix[0][1]*center.Y + matrix[0][2]*center.Z + matrix[0][3]/1000.0
        gy = matrix[1][0]*center.X + matrix[1][1]*center.Y + matrix[1][2]*center.Z + matrix[1][3]/1000.0
        gz = matrix[2][0]*center.X + matrix[2][1]*center.Y + matrix[2][2]*center.Z + matrix[2][3]/1000.0
        
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
            # 방향 벡터 회전 변환 (Translation 제외)
            nz_x = matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z
            nz_y = matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z
            nz_z = matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            data["axis"] = [round(nz_x, 6), round(nz_y, 6), round(nz_z, 6)]
    except: pass
    return data

def walk_hierarchy(part, current_matrix, results):
    # 1. 현재 파트의 바디 수집
    for body in part.Bodies:
        results.append((body, current_matrix))
    
    # 2. 자식 컴포넌트 탐색
    for comp in part.Components:
        t = comp.TransformToRoot
        m = t.Matrix
        # 루트 기준 절대 행렬 구성
        new_matrix = [
            [m.M11, m.M12, m.M13, t.Translation.X * 1000.0],
            [m.M21, m.M22, m.M23, t.Translation.Y * 1000.0],
            [m.M31, m.M32, m.M33, t.Translation.Z * 1000.0]
        ]
        walk_hierarchy(comp.Template, new_matrix, results)

def extract_geometry():
    print("--- SCDM Deep Hierarchy Scan (v4.62) ---")
    all_bodies_raw = []
    try:
        root = GetRootPart()
        if not root:
            try: root = Application.GetActiveDocument().MainPart
            except: pass
        
        if not root:
            print(" - [ERROR] No Active Part found.")
            return [], [], "mm"
            
        print(" - Scanning Root: " + root.Name)
        identity = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
        walk_hierarchy(root, identity, all_bodies_raw)
        
    except Exception as e:
        print(" - [ERROR] Extraction Failed: " + str(e))
        return [], [], "mm"
    
    # 중복 제거
    unique_bodies = []
    seen = set()
    for b, m in all_bodies_raw:
        h = b.GetHashCode()
        if h not in seen:
            unique_bodies.append((b, m))
            seen.add(h)
            
    print(" - Total Bodies Found: {0}".format(len(unique_bodies)))
    final_data = []
    for i, (body, matrix) in enumerate(unique_bodies):
        try:
            b_name = "Body_" + str(i)
            try: b_name = body.Name
            except: pass
            
            vol = 0.0
            try: vol = body.Shape.Volume * 1e9
            except: pass
            
            bdata = {"body_index": i, "body_name": b_name, "volume": vol, "faces": []}
            for face in list(body.Faces):
                bdata["faces"].append(get_face_data(face, matrix))
            final_data.append(bdata)
            print("   [OK] Body: '{0}' (Index: {1})".format(b_name, i))
        except: pass
            
    return final_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction completed successfully.")
except Exception as e: print("\n[FATAL] " + str(e))
