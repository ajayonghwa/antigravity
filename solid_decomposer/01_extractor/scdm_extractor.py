# -*- coding: utf-8 -*-
import json
import os
import clr
import sys

try:
    clr.AddReference("SpaceClaim.Api.V22")
    import SpaceClaim.Api.V22 as sc
except Exception as e:
    print("[FATAL] SpaceClaim API V22 Load Error: " + str(e))
    sys.exit()

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
                # [v4.13] GetAllBodies()로 얻은 바디의 면은 이미 월드 좌표계 기준입니다.
                data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                data["normal"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]

        # Bounding Box
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Native World Extraction (v4.13) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    # [v4.13] 수동 변환(Transform) 계산을 버리고, 
    # 루트 파트에서 직접 모든 인스턴스 바디를 월드 좌표계 상태로 가져옵니다. (안정 버전 방식 복구)
    try:
        bodies = root.GetAllBodies()
    except:
        try:
            bodies = root.Bodies
        except Exception as e:
            print(" - [FATAL] Failed to get bodies: " + str(e))
            return [], [], "m"
            
    print(" - Found {0} bodies".format(bodies.Count if hasattr(bodies, "Count") else len(list(bodies))))

    for i, body in enumerate(bodies):
        try:
            bname = body.Name
            uname = "AUTO_BODY_" + str(i)
            # body.Name = uname # (선택사항) 원본 이름을 유지하려면 이 줄을 주석 처리할 수 있으나 플래너 호환성을 위해 유지
            
            body_data = {
                "body_index": i, "body_name": uname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": [], "adjacency": []
            }

            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face)
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
