# -*- coding: utf-8 -*-
import json
import os
import clr
import sys

try:
    clr.AddReference("SpaceClaim.Api.V22")
    import SpaceClaim.Api.V22 as scapi
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
                # GetDescendants로 얻은 바디의 Frame은 자동 월드 좌표
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
    print("--- SCDM Native Descendant Extraction (v4.14) ---")
    all_bodies_data = []
    root = GetRootPart()
    if not root: return [], [], "m"
    
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass

    bodies_list = []
    
    # [v4.14] V22에 맞춘 완벽한 네이티브 계층 순회 (Transform 에러 원천 차단)
    # 1. 최상위(Root) 바디 수집
    try:
        for b in root.Bodies:
            bodies_list.append(b)
    except Exception as e:
        print(" - [WARN] Failed to get root bodies: " + str(e))
        
    # 2. 모든 하위 컴포넌트의 바디 수집 (GetDescendants 사용)
    try:
        # V22의 GetDescendants는 제네릭 메서드로 IDesignBody를 찾습니다.
        descendants = root.GetDescendants[scapi.IDesignBody]()
        for b in descendants:
            # 중복 방지 (루트 바디 제외)
            if b not in bodies_list:
                bodies_list.append(b)
    except Exception as e:
        print(" - [WARN] GetDescendants failed, using recursive fallback...")
        # 3. 최후의 보루: V22용 안전한 재귀 수집기 (리스트형 Transform 누적 방식)
        def collect_safe(part, transform_list, target_list):
            for c in part.Components:
                if c.Template:
                    current_transforms = list(transform_list)
                    current_transforms.append(c.Transform)
                    
                    for b in c.Template.Bodies:
                        # [핵심] 템플릿 바디를 직접 넣지 않고 Transform 정보와 함께 보존
                        target_list.append((b, current_transforms))
                        
                    collect_safe(c.Template, current_transforms, target_list)
        
        safe_body_infos = []
        for b in root.Bodies:
            safe_body_infos.append((b, []))
        collect_safe(root, [], safe_body_infos)
        
        # 만약 GetDescendants가 실패했다면 이 방식으로 반환값을 가공해야 하므로 안내 출력
        print(" - [INFO] Found {0} bodies via safe recursion.".format(len(safe_body_infos)))
        bodies_list = safe_body_infos # 튜플 리스트로 변환됨

    print(" - Found {0} total bodies".format(len(bodies_list)))

    # 바디 정보 추출
    for i, item in enumerate(bodies_list):
        try:
            # item이 (body, transform_list) 튜플인지, 단일 body 객체인지 판별
            if isinstance(item, tuple):
                body, t_list = item
                is_tuple = True
            else:
                body = item
                t_list = []
                is_tuple = False
                
            bname = body.Name
            uname = "AUTO_BODY_" + str(i)
            # body.Name = uname # (선택) 컴포넌트 안의 템플릿 이름이 바뀔 수 있어 이번엔 생략
            
            body_data = {
                "body_index": i, "body_name": bname, "original_name": bname,
                "volume": getattr(body.Shape, "Volume", 0.0),
                "faces": [], "adjacency": []
            }

            for j, face in enumerate(list(body.Faces)):
                fdata = get_face_data(face)
                
                # [v4.14] 재귀 방식(튜플)으로 수집된 경우, 점진적 Transform 적용 (Matrix 단어 없음)
                if is_tuple and len(t_list) > 0:
                    def apply_t(pt_dir):
                        res = pt_dir
                        for t in reversed(t_list):
                            res = t * res
                        return res
                    
                    fdata["origin"] = [apply_t(scapi.Point.Create(*fdata["origin"])).X, 
                                       apply_t(scapi.Point.Create(*fdata["origin"])).Y, 
                                       apply_t(scapi.Point.Create(*fdata["origin"])).Z]
                    if "axis" in fdata:
                        fdata["axis"] = [apply_t(scapi.Direction.Create(*fdata["axis"])).X, 
                                         apply_t(scapi.Direction.Create(*fdata["axis"])).Y, 
                                         apply_t(scapi.Direction.Create(*fdata["axis"])).Z]
                    if "normal" in fdata:
                        fdata["normal"] = [apply_t(scapi.Direction.Create(*fdata["normal"])).X, 
                                           apply_t(scapi.Direction.Create(*fdata["normal"])).Y, 
                                           apply_t(scapi.Direction.Create(*fdata["normal"])).Z]
                    
                    # Box 변환 (단순화)
                    if fdata["box"]["max"] != [0,0,0]:
                        p1 = apply_t(scapi.Point.Create(*fdata["box"]["min"]))
                        p2 = apply_t(scapi.Point.Create(*fdata["box"]["max"]))
                        fdata["box"]["min"] = [min(p1.X, p2.X), min(p1.Y, p2.Y), min(p1.Z, p2.Z)]
                        fdata["box"]["max"] = [max(p1.X, p2.X), max(p1.Y, p2.Y), max(p1.Z, p2.Z)]

                fdata["index"] = j
                body_data["faces"].append(fdata)
            
            all_bodies_data.append(body_data)
            print(" - [OK] {0}".format(bname))
        except Exception as e:
            print(" - [ERROR] {0}: {1}".format(bname, str(e)))
            
    return all_bodies_data, [], unit_str

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": uinfo, "warnings": warns, "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Geometry data saved.")
except Exception as e: print("\n[FATAL] " + str(e))
