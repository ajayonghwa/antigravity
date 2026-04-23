# -*- coding: utf-8 -*-
import json
import os
import clr

def load_scdm_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        from SpaceClaim.Api.V22 import Matrix, Point, Direction, Frame, Component, Selection
        return Matrix, Point, Direction, Frame, Component, Selection
    except: return None

# API 클래스들을 전역으로 로드
api_classes = load_scdm_api()
if api_classes:
    Matrix, Point, Direction, Frame, Component, Selection = api_classes
else:
    print("[FATAL] Failed to load SpaceClaim API V22")

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, world_matrix):
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
                # 월드 좌표로 변환
                w_origin = world_matrix * f.Origin
                w_axis = world_matrix * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["axis"] = [w_axis.X, w_axis.Y, w_axis.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                w_origin = world_matrix * f.Origin
                w_normal = world_matrix * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["normal"] = [w_normal.X, w_normal.Y, w_normal.Z]

        # Bounding Box (변환 적용)
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            p1 = world_matrix * r.Min
            p2 = world_matrix * r.Max
            data["box"]["min"] = [min(p1.X, p2.X), min(p1.Y, p2.Y), min(p1.Z, p2.Z)]
            data["box"]["max"] = [max(p1.X, p2.X), max(p1.Y, p2.Y), max(p1.Z, p2.Z)]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Robust World Extraction (v4.10) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    def collect_with_transform(part, current_m, blist):
        # 바디 수집
        for b in part.Bodies:
            blist.append((b, current_m))
        # 하위 컴포넌트 재귀 탐색
        for c in part.Components:
            if c.Template:
                # 계층적 변환 매트릭스 누적 (Matrix.Create()를 통한 안전한 복제 및 곱셈)
                new_m = current_m * c.Transform.Matrix
                collect_with_transform(c.Template, new_m, blist)
    
    bodies_info = []
    # 초기 매트릭스는 Identity
    collect_with_transform(root, Matrix.Identity, bodies_info)
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
            print(" - [OK] {0} (World Matrix Applied)".format(uname))
        except Exception as e:
            print(" - [ERROR] {0}: {1}".format(body.Name, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] " + str(e))
