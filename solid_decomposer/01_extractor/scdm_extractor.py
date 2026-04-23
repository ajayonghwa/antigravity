# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.65] 극한의 반경 추출 로직 (속성 전수 조사 + 바운딩 박스 추론)
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
except Exception as e:
    print(" - [ERROR] API Load Failed: " + str(e))

if 'OUTPUT_PATH' not in globals():
    OUTPUT_PATH = r"D:\yhheo\py_programs_by_yh\solid_decomposer\data\geometry_data.json"

def get_face_data(face, matrix_obj):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        
        # 1. 루트 기준 좌표 및 바운딩 박스
        bbox = face.GetBoundingBox(matrix_obj)
        c = bbox.Center
        data["origin"] = [round(c.X * 1000.0, 8), round(c.Y * 1000.0, 8), round(c.Z * 1000.0, 8)]
        
        # 2. 극한의 반경 추출 로직
        r = 0.0
        # 방식 A: 면 속성 전수 조사
        for r_attr in ["Radius", "Radius0", "MajorRadius", "MinorRadius"]:
            if hasattr(geom, r_attr):
                r_val = getattr(geom, r_attr)
                if r_val > 0: r = r_val; break
        
        # 방식 B: 모서리(Edge) 기하 정보 조사
        if r <= 0:
            for edge in face.Edges:
                e_geom = edge.Shape.Geometry
                for r_attr in ["Radius", "Radius0", "MajorRadius"]:
                    if hasattr(e_geom, r_attr):
                        r_val = getattr(e_geom, r_attr)
                        if r_val > 0: r = r_val; break
                if r > 0: break
                
        # 방식 C: 기하학적 추론 (바운딩 박스 크기 활용)
        if r <= 0:
            # 로컬 바운딩 박스에서 가로/세로 크기 측정
            local_bbox = face.GetBoundingBox(Matrix.Identity)
            dx = local_bbox.Size.X
            dy = local_bbox.Size.Y
            dz = local_bbox.Size.Z
            # 원통 구멍이라면 세 축 중 두 축은 지름(2R)과 비슷해야 함
            dims = sorted([dx, dy, dz])
            if dims[0] > 0 and abs(dims[0] - dims[1]) / dims[0] < 0.05: # 두 변의 차이가 5% 이내면 원형으로 간주
                r = dims[0] / 2.0
                print("   [INFER] Radius inferred from bbox: {0:.4f}mm".format(r*1000.0))

        if r > 0:
            data["radius"] = round(r * 1000.0, 8)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
            
        # 3. 축(Axis) 계산
        if hasattr(geom, "Frame"):
            f = geom.Frame
            m = matrix_obj
            nz_x = m.M11*f.DirZ.X + m.M12*f.DirZ.Y + m.M13*f.DirZ.Z
            nz_y = m.M21*f.DirZ.X + m.M22*f.DirZ.Y + m.M23*f.DirZ.Z
            nz_z = m.M31*f.DirZ.X + m.M32*f.DirZ.Y + m.M33*f.DirZ.Z
            data["axis"] = [round(nz_x, 8), round(nz_y, 8), round(nz_z, 8)]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Extreme Radius Extraction (v4.65) ---")
    final_bodies_data = []
    try:
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        if not root: return [], [], "mm"
        
        all_bodies = list(root.GetDescendants[IDesignBody]())
        if not all_bodies:
            all_bodies = list(root.Bodies)
            for comp in root.Components:
                for b in comp.Template.Bodies: all_bodies.append(b)

        print(" - Processing {0} body occurrences...".format(len(all_bodies)))
        
        for i, body in enumerate(all_bodies):
            try:
                b_name = getattr(body, "Name", "Body_" + str(i))
                total_matrix = Matrix.Identity
                if body.Instance: total_matrix = body.TransformToMaster.Inverse
                
                vol = 0.0
                try: vol = body.Shape.Volume * 1e9
                except: pass
                
                bdata = {"body_index": i, "body_name": b_name, "volume": vol, "faces": []}
                for face in list(body.Faces):
                    bdata["faces"].append(get_face_data(face, total_matrix))
                
                final_bodies_data.append(bdata)
                print("   [OK] {0} (Faces: {1})".format(b_name, len(body.Faces)))
            except: pass
                
    except Exception as e: print(" - [FATAL] Loop Failed: " + str(e))
    return final_bodies_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Extraction complete. Extreme detection applied.")
except Exception as e: print("\n[FATAL] " + str(e))
