# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.58] 엣지 기반 반경 추출 (면 정보가 누락된 NURBS 대응)
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
        
        # 바운딩 박스 및 중심점 (mm 변환: m * 1000)
        bbox = face.GetBoundingBox(Matrix.Identity)
        data["origin"] = [round(bbox.Center.X * 1000.0, 6), round(bbox.Center.Y * 1000.0, 6), round(bbox.Center.Z * 1000.0, 6)]
        data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
        data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]

        # 1차 시도: 면의 기하 정보에서 직접 추출
        r = 0.0
        if hasattr(geom, "Radius"): r = geom.Radius
        elif hasattr(geom, "Radius0"): r = geom.Radius0
        
        # 2차 시도: 엣지 전수 조사 (NURBS 실린더 대응)
        if r <= 0:
            for edge in face.Edges:
                e_geom = edge.Shape.Geometry
                if hasattr(e_geom, "Radius"):
                    r = e_geom.Radius
                    print("   [INFO] Edge-based radius found: {0:.4f}mm".format(r*1000.0))
                    break
        
        if r > 0:
            data["radius"] = round(r * 1000.0, 6)
            # 내부 구멍 여부 판단
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
        # 축(Axis) 계산
        if hasattr(geom, "Frame"):
            f = geom.Frame
            data["axis"] = [
                round(matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, 6),
                round(matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[2][0]*f.DirZ.Z, 6),
                round(matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z, 6)
            ]
    except Exception as fe:
        print("   [WARN] Face extraction error: " + str(fe))
        
    return data

def extract_geometry():
    print("--- SCDM Deep Extraction (v4.58) ---")
    all_bodies_data = []
    try: root = GetRootPart()
    except: return [], [], "mm"
    
    bodies = list(root.GetDescendants[IDesignBody]())
    if not bodies: bodies = list(root.Bodies)
    
    for i, body in enumerate(bodies):
        # 변환 행렬 가져오기
        matrix_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        try:
            comp = body.ParentComponent
            if comp:
                t = comp.TransformToRoot
                matrix_py[0][3] = t.Translation.X * 1000.0
                matrix_py[1][3] = t.Translation.Y * 1000.0
                matrix_py[2][3] = t.Translation.Z * 1000.0
        except: pass
        
        body.Name = "AUTO_BODY_" + str(i)
        vol = 0.0
        try: vol = body.Shape.Volume * 1e9
        except: pass
        
        bdata = {"body_index": i, "body_name": body.Name, "volume": vol, "faces": []}
        for j, face in enumerate(list(body.Faces)):
            bdata["faces"].append(get_face_data(face, matrix_py))
        all_bodies_data.append(bdata)
        print(" - Body '{0}' extraction complete.".format(body.Name))
            
    return all_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete. Units fixed to mm.")
except Exception as e: print("\n[FATAL] " + str(e))
