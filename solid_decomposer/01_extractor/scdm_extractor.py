# -*- coding: utf-8 -*-
import json
import os

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, matrix):
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
                
                # [v4.23] Matrix 곱셈 연산자(*) 대신 명시적 Transform 메서드 사용
                if matrix is not None:
                    try:
                        # SpaceClaim Matrix 객체의 Transform 메서드 시도
                        w_origin = matrix.Transform(f.Origin)
                        w_axis = matrix.Transform(f.DirZ)
                        data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                        data["axis"] = [w_axis.X, w_axis.Y, w_axis.Z]
                    except:
                        # 실패시 연산자 시도
                        try:
                            w_origin = matrix * f.Origin
                            data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                        except:
                            data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                else:
                    data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                    data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
            
            elif "Plane" in g_type:
                f = geom.Frame
                if matrix is not None:
                    try:
                        w_origin = matrix.Transform(f.Origin)
                        w_normal = matrix.Transform(f.DirZ)
                        data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                        data["normal"] = [w_normal.X, w_normal.Y, w_normal.Z]
                    except:
                        data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                else:
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
    print("--- SCDM Matrix Transform Extraction (v4.23) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    bodies_info = []
    def get_all_occurrences(part, current_matrix):
        # 최상위 바디들
        for b in part.Bodies:
            bodies_info.append((b, current_matrix))
        # 컴포넌트 하위 바디들
        for c in part.Components:
            try:
                # c.Placement (Matrix)
                m = c.Placement
                if current_matrix is None:
                    next_matrix = m
                else:
                    # Matrix 곱셈 (연산자 혹은 Multiply)
                    try: next_matrix = current_matrix * m
                    except: next_matrix = m
            except:
                next_matrix = current_matrix
                
            if hasattr(c, "Template") and c.Template:
                get_all_occurrences(c.Template, next_matrix)

    get_all_occurrences(root, None)
    print(" - Found {0} bodies".format(len(bodies_info)))

    for i, (body, matrix) in enumerate(bodies_info):
        try:
            bname = body.Name
            body_data = {
                "body_index": i, "body_name": bname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": []
            }
            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face, matrix)
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
