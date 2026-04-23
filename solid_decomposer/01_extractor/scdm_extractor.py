# -*- coding: utf-8 -*-
import json
import os
import clr
import math

# [1] SpaceClaim API 참조 추가 (가장 확실한 방식)
def load_scdm_api():
    try:
        # V22를 우선적으로 시도
        clr.AddReference("SpaceClaim.Api.V22")
        import SpaceClaim.Api.V22 as scapi
        return scapi
    except:
        # 하위 버전 Fallback
        for v in range(21, 16, -1):
            try:
                ref = "SpaceClaim.Api.V" + str(v)
                clr.AddReference(ref)
                import SpaceClaim.Api.V22 as scapi # 참조 로드 후에는 scapi로 별칭
                return scapi
            except: pass
    return None

scapi = load_scdm_api()

# [사용자 설정]
if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face):
    """
    면(Face) 정보 추출 - 속성 유무를 철저히 검사하여 안정성 확보
    """
    data = {
        "id": 0, "type": "Unknown", "area": 0.0,
        "box": {"min": [0,0,0], "max": [0,0,0]}
    }
    
    try:
        # Id 및 Area 추출
        if hasattr(face, "Id"): data["id"] = face.Id
        
        # Shape 객체 접근 (DesignFace일 경우 대비)
        shape = face
        if hasattr(face, "Shape"): shape = face.Shape
        
        if hasattr(shape, "Area"): data["area"] = shape.Area
        
        # Bounding Box
        r = None
        if hasattr(shape, "Range"): r = shape.Range
        elif hasattr(face, "Box"): r = face.Box
        
        if r:
            data["box"]["min"] = [r.Min.X, r.Min.Y, r.Min.Z]
            data["box"]["max"] = [r.Max.X, r.Max.Y, r.Max.Z]

        # 기하 타입 분석
        if hasattr(shape, "Geometry"):
            geom = shape.Geometry
            g_type = geom.GetType().Name
            data["type"] = g_type
            
            # 공통 프레임 정보
            frame = None
            if hasattr(geom, "Frame"): frame = geom.Frame
            
            # 실린더/원추
            if "Cylinder" in g_type or "Conical" in g_type:
                if hasattr(geom, "Radius"): data["radius"] = geom.Radius
                
                # [v4.2] 지오메트리 원점을 명시적으로 저장 (가장 중요)
                if frame:
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                
                # 내경 판별
                data["is_internal"] = False
                if hasattr(shape, "Orientation"):
                    if str(shape.Orientation) == "Reversed":
                        data["is_internal"] = True
            
            # 평면
            elif "Plane" in g_type:
                if frame:
                    data["normal"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                    
            # 토로이달
            elif "Toroidal" in g_type:
                if hasattr(geom, "MajorRadius"): data["radius"] = geom.MajorRadius
                if frame:
                    data["origin"] = [frame.Origin.X, frame.Origin.Y, frame.Origin.Z]
                    data["axis"] = [frame.DirZ.X, frame.DirZ.Y, frame.DirZ.Z]
    except Exception as e:
        print("  ! Face extraction error: " + str(e))
        
    return data

def extract_geometry():
    print("--- SCDM Detailed Extraction Engine (v3.6) ---")
    all_bodies_data = []
    warnings = []
    
    root = GetRootPart()
    if not root:
        return [], ["No active part found."]

    # 단위 정보
    unit_str = "m"
    try: unit_str = str(root.Document.Units.Length.Symbol)
    except: pass
    print(" - Units: " + unit_str)

    # 모든 바디 수집 (재귀)
    def collect(part, blist):
        for b in part.Bodies: blist.append(b)
        for c in part.Components:
            if c.Template: collect(c.Template, blist)
    
    bodies = []
    collect(root, bodies)
    print(" - Total bodies: {0}".format(len(bodies)))

    for i, body in enumerate(bodies):
        try:
            # 기본 식별
            bname = "Unknown"
            try: bname = body.GetFullName()
            except: bname = body.Name
            
            uname = "AUTO_BODY_" + str(i)
            try: body.Name = uname
            except: pass
            
            vol = 0.0
            try: vol = body.Shape.Volume
            except: vol = getattr(body, "Volume", 0.0)

            body_data = {
                "body_index": i,
                "body_name": uname,
                "original_name": bname.replace("\\", "/"),
                "volume": vol,
                "faces": [],
                "adjacency": [],
                "identified_holes": []
            }

            # 면 데이터
            face_list = []
            try: face_list = list(body.Faces)
            except: face_list = list(body.Shape.Faces)
            
            fmap = {}
            for j, face in enumerate(face_list):
                fdata = get_face_data(face)
                fdata["index"] = j
                body_data["faces"].append(fdata)
                fmap[face] = j
            
            # 인접성
            try:
                edge_list = []
                try: edge_list = body.Edges
                except: edge_list = body.Shape.Edges
                for e in edge_list:
                    if e.Faces.Count == 2:
                        idx1 = fmap.get(e.Faces[0])
                        idx2 = fmap.get(e.Faces[1])
                        if idx1 is not None and idx2 is not None:
                            body_data["adjacency"].append([idx1, idx2])
            except: pass

            # 홀 식별 (V22 전용 API 시도)
            try:
                # 네임스페이스를 동적으로 확인하여 접근
                if scapi:
                    try:
                        # IdentifyHoleOptions 위치가 버전마다 다를 수 있음
                        opt_class = None
                        try: opt_class = scapi.IdentifyHoleOptions
                        except: 
                            try: opt_class = scapi.Modeler.IdentifyHoleOptions
                            except: pass
                        
                        if opt_class:
                            options = opt_class()
                            holes = body.IdentifyHoles(options)
                            for h in holes:
                                hdata = {
                                    "type": "Through" if h.Through else "Blind",
                                    "diameter": h.DrillSize, "depth": h.Depth
                                }
                                try:
                                    hdata["axis"] = [h.Axis.Direction.X, h.Axis.Direction.Y, h.Axis.Direction.Z]
                                    hdata["origin"] = [h.Axis.Origin.X, h.Axis.Origin.Y, h.Axis.Origin.Z]
                                except: pass
                                body_data["identified_holes"].append(hdata)
                    except: pass
            except: pass

            all_bodies_data.append(body_data)
            print(" - [OK] {0}: {1} faces".format(uname, len(body_data["faces"])))
            
        except Exception as e:
            err = "Error processing body {0}: {1}".format(i, str(e))
            print(" !! " + err)
            warnings.append(err)
            
    return all_bodies_data, warnings, unit_str

# 실행
try:
    results, warns, uinfo = extract_geometry()
    final = {
        "sub_device_name": "DEVICE",
        "units": uinfo,
        "warnings": warns,
        "bodies": results
    }
    
    tdir = os.path.dirname(OUTPUT_PATH)
    if tdir and not os.path.exists(tdir): os.makedirs(tdir)
    
    with open(OUTPUT_PATH, "w") as f:
        json.dump(final, f, indent=2)
    print("\n[FINISH] Data saved to: " + OUTPUT_PATH)
except Exception as e:
    print("\n[FATAL] " + str(e))
