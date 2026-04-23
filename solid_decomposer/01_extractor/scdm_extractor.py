# -*- coding: utf-8 -*-
import json
import os
import clr
import sys

# [v4.12] Matrix 클래스 충돌을 피하기 위해 최상위 네임스페이스만 로드
try:
    clr.AddReference("SpaceClaim.Api.V22")
    import SpaceClaim.Api.V22 as sc
except Exception as e:
    print("[FATAL] SpaceClaim API V22 Load Error: " + str(e))
    sys.exit()

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, transform_obj):
    '''지중된 변환 객체를 사용하여 월드 좌표 추출'''
    data = {
        "id": 0, "type": "Unknown", "area": 0.0, 
        "box": {"min": [0,0,0], "max": [0,0,0]},
        "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False
    }
    try:
        if hasattr(face, "Id"): data["id"] = face.Id
        shape = face.Shape if hasattr(face, "Shape") else face
        
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                f = geom.Frame
                # [v4.12] 별도의 Matrix 연산 없이 Transform 객체로 직접 변환
                w_origin = transform_obj * f.Origin
                w_axis = transform_obj * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["axis"] = [w_axis.X, w_axis.Y, w_axis.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                w_origin = transform_obj * f.Origin
                w_normal = transform_obj * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["normal"] = [w_normal.X, w_normal.Y, w_normal.Z]

        # Bounding Box (변환 적용)
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            p1 = transform_obj * r.Min
            p2 = transform_obj * r.Max
            data["box"]["min"] = [min(p1.X, p2.X), min(p1.Y, p2.Y), min(p1.Z, p2.Z)]
            data["box"]["max"] = [max(p1.X, p2.X), max(p1.Y, p2.Y), max(p1.Z, p2.Z)]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Direct-Transform Extraction (v4.12) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    # [v4.12] Matrix를 직접 다루지 않고 Component의 Transform 객체를 활용
    def collect_bodies_with_context(part, context_transform, blist):
        for b in part.Bodies:
            blist.append((b, context_transform))
        for c in part.Components:
            if c.Template:
                # Transform 객체끼리의 곱셈은 Matrix 에러로부터 자유로움
                new_transform = context_transform * c.Transform
                collect_bodies_with_context(c.Template, new_transform, blist)
    
    bodies_info = []
    # 초기 변환은 Identity Transform
    collect_bodies_with_context(root, sc.Transform.Identity, bodies_info)
    print(" - Found {0} bodies".format(len(bodies_info)))

    for i, (body, body_transform) in enumerate(bodies_info):
        try:
            bname = body.Name
            uname = "AUTO_BODY_" + str(i)
            body.Name = uname
            
            body_data = {
                "body_index": i, "body_name": uname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": [], "adjacency": []
            }

            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face, body_transform)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            
            all_bodies_data.append(body_data)
            print(" - [OK] {0}".format(uname))
        except Exception as e:
            print(" - [ERROR] {0}: {1}".format(body.Name, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] " + str(e))
