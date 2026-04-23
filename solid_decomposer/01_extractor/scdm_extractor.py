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
                
                # [v4.22] Placement(Matrix)를 사용해 점/벡터를 변환합니다.
                if matrix is not None:
                    try:
                        w_origin = matrix * f.Origin
                        w_axis = matrix * f.DirZ
                        data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                        data["axis"] = [w_axis.X, w_axis.Y, w_axis.Z]
                    except:
                        data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                        data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                else:
                    data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                    data["axis"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                if matrix is not None:
                    try:
                        w_origin = matrix * f.Origin
                        w_normal = matrix * f.DirZ
                        data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                        data["normal"] = [w_normal.X, w_normal.Y, w_normal.Z]
                    except:
                        data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                        data["normal"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]
                else:
                    data["origin"] = [f.Origin.X, f.Origin.Y, f.Origin.Z]
                    data["normal"] = [f.DirZ.X, f.DirZ.Y, f.DirZ.Z]

        # Bounding Box (단순화: 포인트 매트릭스 변환)
        r = getattr(shape, "Range", getattr(face, "Box", getattr(face, "BoundingBox", None)))
        if r:
            if matrix is not None:
                try:
                    p1 = matrix * r.Min
                    p2 = matrix * r.Max
                    data["box"]["min"] = [min(p1.X, p2.X), min(p1.Y, p2.Y), min(p1.Z, p2.Z)]
                    data["box"]["max"] = [max(p1.X, p2.X), max(p1.Y, p2.Y), max(p1.Z, p2.Z)]
                except:
                    data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
                    data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
            else:
                data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
                data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Placement Extraction (v4.22) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    # [v4.22] c.Transform은 API V22에서 더이상 Component의 변환행렬이 아니며 네임스페이스 에러를 유발합니다.
    # 정확한 V22 속성인 c.Placement(Matrix 객체)를 사용해 누적 변환 행렬을 계산합니다.
    bodies_info = []
    def get_all_occurrences(part, current_matrix):
        for b in part.Bodies:
            bodies_info.append((b, current_matrix))
        for c in part.Components:
            try:
                # c.Placement는 마스터 템플릿에서 부모 파트로의 Matrix입니다.
                if current_matrix is None:
                    next_matrix = c.Placement
                else:
                    next_matrix = current_matrix * c.Placement
            except:
                next_matrix = current_matrix
                
            if hasattr(c, "Template") and c.Template:
                get_all_occurrences(c.Template, next_matrix)

    try:
        get_all_occurrences(root, None)
    except Exception as e:
        print(" - [FATAL] Failed to collect occurrences: " + str(e))
            
    print(" - Found {0} bodies".format(len(bodies_info)))

    for i, (body, matrix) in enumerate(bodies_info):
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
