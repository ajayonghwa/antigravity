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
    print("--- SCDM Modeler Extraction (v4.24) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    # [v4.24] Modeler 네임스페이스를 명시적으로 로드하여 GetAllBodies() 확장 메서드 활성화 시도
    import clr
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        from SpaceClaim.Api.V22.Modeler import Body as ModelerBody
    except: pass

    bodies = []
    try:
        # [최종 수단] GetAllBodies()가 존재하는지 확인
        bodies = list(root.GetAllBodies())
        print(" - Successfully used GetAllBodies()")
    except:
        # 실패시 수동 계층 탐색 (World Coordinate 인스턴스 추출)
        print(" - GetAllBodies failed, falling back to GetDescendants")
        try:
            # V22에서는 GetDescendants[IDesignBody]()가 인스턴스를 반환할 수도 있음
            from SpaceClaim.Api.V22 import IDesignBody
            bodies = list(root.GetDescendants[IDesignBody]())
        except:
            bodies = list(root.Bodies)

    print(" - Found {0} bodies".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            bname = body.Name
            body_data = {
                "body_index": i, "body_name": bname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": []
            }
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            all_bodies_data.append(body_data)
            print(" - [OK] Processed: {0}".format(bname))
        except Exception as e:
            print(" - [ERROR] Failed on {0}: {1}".format(body.Name, str(e)))
            
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] Outer error: " + str(e))
