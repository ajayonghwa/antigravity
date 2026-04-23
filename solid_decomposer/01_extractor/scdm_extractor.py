# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face):
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
                data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                data["normal"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]

        # Bounding Box
        r = getattr(shape, "Range", getattr(face, "Box", getattr(face, "BoundingBox", None)))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Native Content Extraction (v4.19) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    # [v4.19] GetAllBodies() 의존성 제거, 가장 완벽한 Content 기반 재귀 탐색
    # 컴포넌트의 Template(마스터/로컬좌표) 대신 Content(인스턴스/월드좌표)를 순회합니다.
    bodies = []
    def get_all_occurrences(part_occurrence, b_list):
        for b in part_occurrence.Bodies:
            b_list.append(b)
        for c in part_occurrence.Components:
            # c.Content는 부모 컨텍스트를 유지하는 IPart 인스턴스이므로
            # 여기서 뽑아낸 바디는 자동으로 월드 좌표계를 가집니다.
            if hasattr(c, "Content") and c.Content:
                get_all_occurrences(c.Content, b_list)
            else:
                # Content 속성이 없는 버전에 대비 (가상 컴포넌트 등)
                if hasattr(c, "Template") and c.Template:
                    get_all_occurrences(c.Template, b_list)

    try:
        get_all_occurrences(root, bodies)
    except Exception as e:
        print(" - [FATAL] Failed to collect occurrences: " + str(e))
            
    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            bname = body.Name
            uname = "AUTO_BODY_" + str(i)
            # body.Name = uname # (선택) 원래 이름 보존
            
            body_data = {
                "body_index": i, "body_name": bname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": [], "adjacency": []
            }

            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            
            all_bodies_data.append(body_data)
            print(" - [OK] Processed: {0}".format(bname))
        except Exception as e:
            print(" - [ERROR] Failed on {0}: {1}".format(body.Name, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] Outer error: " + str(e))
