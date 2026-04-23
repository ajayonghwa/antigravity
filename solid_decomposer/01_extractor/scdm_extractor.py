# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_world_point(face, local_pt):
    # [v4.25] 매트릭스 계산을 포기하고, 스페이스클레임 내장 GetBoundingBox(Identity) 기능을 이용해 
    # 페이스의 월드 좌표 중심을 직접 구합니다. 이것이 가장 확실한 월드 좌표 추출법입니다.
    try:
        from SpaceClaim.Api.V22.Geometry import Matrix
        bbox = face.GetBoundingBox(Matrix.Identity)
        center = bbox.Center
        return [center.X, center.Y, center.Z]
    except:
        return [local_pt.X, local_pt.Y, local_pt.Z]

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
            
            # 월드 좌표 중심으로 Origin 추출
            f = geom.Frame
            data["origin"] = get_world_point(face, f.Origin)
            
            if "Cylinder" in g_type or "Conical" in g_type:
                data["radius"] = getattr(geom, "Radius", 0.0)
                # 축(Axis)은 로컬과 월드가 회전이 없다면 동일하므로 일단 유지
                data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                data["normal"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]

        # 월드 기준 Bounding Box
        try:
            from SpaceClaim.Api.V22.Geometry import Matrix
            wb = face.GetBoundingBox(Matrix.Identity)
            data["box"]["min"] = [wb.Min.X, wb.Min.Y, wb.Min.Z]
            data["box"]["max"] = [wb.Max.X, wb.Max.Y, wb.Max.Z]
        except:
            r = getattr(shape, "Range", getattr(face, "Box", getattr(face, "BoundingBox", None)))
            if r:
                data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
                data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM BoundingBox World Extraction (v4.25) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    # 1. 모든 바디 인스턴스 수집 (GetDescendants 이용)
    from SpaceClaim.Api.V22 import IDesignBody
    try:
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
