# -*- coding: utf-8 -*-
import json
import os
import clr

def load_scdm_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        import SpaceClaim.Api.V22 as scapi
        return scapi
    except: return None

scapi = load_scdm_api()

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_world_transform(occurrence):
    '''컴포넌트 계층을 따라가며 월드 변환 매트릭스 계산'''
    matrix = scapi.Matrix.Identity
    curr = occurrence
    while curr:
        if hasattr(curr, "Transform"):
            matrix = curr.Transform.Matrix * matrix
        curr = curr.Parent
    return matrix

def get_face_data(face, transform):
    data = {
        "id": 0, "type": "Unknown", "area": 0.0, 
        "box": {"min": [0,0,0], "max": [0,0,0]},
        "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False
    }
    try:
        if hasattr(face, "Id"): data["id"] = face.Id
        shape = face.Shape if hasattr(face, "Shape") else face
        
        # [v4.8] 로컬 지오메트리 정보 추출
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                f = geom.Frame
                # 로컬 좌표
                l_origin = f.Origin
                l_axis = f.DirZ
                # 월드 좌표로 변환
                w_origin = transform * l_origin
                w_axis = transform * l_axis
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["axis"] = [w_axis.X, w_axis.Y, w_axis.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                w_origin = transform * f.Origin
                w_normal = transform * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["normal"] = [w_normal.X, w_normal.Y, w_normal.Z]

        # Bounding Box (변환 적용)
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            p1 = transform * r.Min
            p2 = transform * r.Max
            data["box"]["min"] = [min(p1.X, p2.X), min(p1.Y, p2.Y), min(p1.Z, p2.Z)]
            data["box"]["max"] = [max(p1.X, p2.X), max(p1.Y, p2.Y), max(p1.Z, p2.Z)]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM World-Transform Extraction (v4.8) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    def collect_with_transform(part, current_transform, blist):
        # 바디 수집
        for b in part.Bodies:
            blist.append((b, current_transform))
        # 하위 컴포넌트 재귀 탐색
        for c in part.Components:
            if c.Template:
                # 계층적 변환 매트릭스 누적
                new_transform = current_transform * c.Transform
                collect_with_transform(c.Template, new_transform, blist)
    
    bodies_info = []
    collect_with_transform(root, scapi.Matrix.Identity, bodies_info)
    print(" - Found {0} bodies in hierarchy".format(len(bodies_info)))

    for i, (body, transform) in enumerate(bodies_info):
        try:
            bname = body.Name
            uname = "AUTO_BODY_" + str(i)
            body.Name = uname
            
            body_data = {
                "body_index": i, "body_name": uname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": [], "adjacency": []
            }

            face_list = list(body.Faces)
            fmap = {}
            for j, face in enumerate(face_list):
                fdata = get_face_data(face, transform)
                fdata["index"] = j
                body_data["faces"].append(fdata)
                fmap[face] = j
            
            all_bodies_data.append(body_data)
            print(" - [OK] {0} (Transformed to World)".format(uname))
        except Exception as e:
            print(" - [ERROR] {0}: {1}".format(body.Name, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] World-coordinate data saved.")
except Exception as e: print("\n[FATAL] " + str(e))
