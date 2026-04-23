# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.57] 정밀 반경 추출 및 매뉴얼 타입 매칭 강화
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
    print(" - [STEP 1] API V22 Full Load Success")
except Exception as e:
    print(" - [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    # 기본 데이터 구조
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    
    try:
        shape = face.Shape
        geom = shape.Geometry
        g_type_full = str(geom.GetType())
        data["type"] = geom.GetType().Name
        
        # 바운딩 박스 및 중심점 (mm)
        bbox = face.GetBoundingBox(Matrix.Identity)
        data["origin"] = [round(bbox.Center.X * 1000.0, 6), round(bbox.Center.Y * 1000.0, 6), round(bbox.Center.Z * 1000.0, 6)]
        data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
        data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]

        # [v4.57] 반경 추출 강화: Cylinder, Cone 클래스 직접 대조
        r = 0.0
        # 매뉴얼 명세에 따른 프로퍼티 접근
        if hasattr(geom, "Radius"): r = geom.Radius
        elif hasattr(geom, "Radius0"): r = geom.Radius0 # Cone 등
        
        if r > 0:
            data["radius"] = round(r * 1000.0, 6)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
        # 축(Axis) 계산
        if hasattr(geom, "Frame"):
            f = geom.Frame
            data["axis"] = [
                matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z,
                matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z,
                matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z
            ]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Deep Extraction (v4.57) ---")
    all_bodies_data = []
    try: root = GetRootPart()
    except: return [], [], "mm"
    
    bodies = list(root.GetDescendants[IDesignBody]())
    if not bodies: bodies = list(root.Bodies)
    
    print(" - Found {0} bodies".format(len(bodies)))
    for i, body in enumerate(bodies):
        matrix_py = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        try:
            comp = getattr(body, "ParentComponent", None)
            if not comp: comp = getattr(body, "OccurrenceParent", None)
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
            
    return all_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete (mm mode).")
except Exception as e: print("\n[FATAL] " + str(e))
