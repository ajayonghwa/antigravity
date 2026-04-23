# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.11] 최상단에서 명확하게 API 로드
try:
    clr.AddReference("SpaceClaim.Api.V22")
    import SpaceClaim.Api.V22 as scapi
    # 클래스들을 별도 이름으로 할당 (충돌 방지)
    SC_Matrix = scapi.Matrix
    SC_Point = scapi.Point
    SC_Direction = scapi.Direction
    SC_Frame = scapi.Frame
    SC_Component = scapi.Component
    SC_Selection = scapi.Selection
except Exception as e:
    print("[FATAL] SpaceClaim API V22 Load Error: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, m_world):
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
                # 월드 좌표로 변환 (m_world 사용)
                w_origin = m_world * f.Origin
                w_axis = m_world * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["axis"] = [w_axis.X, w_axis.Y, w_axis.Z]
                
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
            elif "Plane" in g_type:
                f = geom.Frame
                w_origin = m_world * f.Origin
                w_normal = m_world * f.DirZ
                data["origin"] = [w_origin.X, w_origin.Y, w_origin.Z]
                data["normal"] = [w_normal.X, w_normal.Y, w_normal.Z]

        # Bounding Box (변환 적용)
        r = getattr(shape, "Range", getattr(face, "Box", None))
        if r:
            p1 = m_world * r.Min
            p2 = m_world * r.Max
            data["box"]["min"] = [min(p1.X, p2.X), min(p1.Y, p2.Y), min(p1.Z, p2.Z)]
            data["box"]["max"] = [max(p1.X, p2.X), max(p1.Y, p2.Y), max(p1.Z, p2.Z)]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Robust World Extraction (v4.11) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    def collect_recursive(part, m_current, blist):
        # 바디 수집
        for b in part.Bodies:
            blist.append((b, m_current))
        # 하위 컴포넌트 탐색
        for c in part.Components:
            if c.Template:
                # 새로운 매트릭스 계산 (복제하여 안전하게 처리)
                m_next = m_current * c.Transform.Matrix
                collect_recursive(c.Template, m_next, blist)
    
    bodies_info = []
    # 초기 매트릭스는 Identity (SC_Matrix 사용)
    collect_recursive(root, SC_Matrix.Identity, bodies_info)
    print(" - Found {0} bodies in hierarchy".format(len(bodies_info)))

    for i, (body, m_world_final) in enumerate(bodies_info):
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
                fdata = get_face_data(face, m_world_final)
                fdata["index"] = j
                body_data["faces"].append(fdata)
            
            all_bodies_data.append(body_data)
            print(" - [OK] {0} (World Coords Extracted)".format(uname))
        except Exception as e:
            print(" - [ERROR] {0}: {1}".format(body.Name, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved successfully.")
except Exception as e: print("\n[FATAL] Outer error: " + str(e))
