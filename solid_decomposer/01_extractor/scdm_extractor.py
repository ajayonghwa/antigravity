# -*- coding: utf-8 -*-
import json
import os
import clr

# [v4.61] 전방위 바디 탐색 (1컴포넌트 1바디 예외 대응)
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

def get_face_data(face, matrix):
    f_id = face.GetHashCode()
    data = {"id": f_id, "type": "Unknown", "area": face.Area * 1e6, "box": {"min": [0,0,0], "max": [0,0,0]}, "origin": [0,0,0], "axis": [0,0,1], "radius": 0.0, "is_internal": False}
    try:
        shape = face.Shape
        geom = shape.Geometry
        data["type"] = geom.GetType().Name
        bbox = face.GetBoundingBox(Matrix.Identity)
        data["origin"] = [round(bbox.Center.X * 1000.0, 6), round(bbox.Center.Y * 1000.0, 6), round(bbox.Center.Z * 1000.0, 6)]
        data["box"]["min"] = [round(bbox.Min.X * 1000.0, 6), round(bbox.Min.Y * 1000.0, 6), round(bbox.Min.Z * 1000.0, 6)]
        data["box"]["max"] = [round(bbox.Max.X * 1000.0, 6), round(bbox.Max.Y * 1000.0, 6), round(bbox.Max.Z * 1000.0, 6)]
        r = 0.0
        if hasattr(geom, "Radius"): r = geom.Radius
        elif hasattr(geom, "Radius0"): r = geom.Radius0
        if r <= 0:
            for edge in face.Edges:
                if hasattr(edge.Shape.Geometry, "Radius"): r = edge.Shape.Geometry.Radius; break
        if r > 0:
            data["radius"] = round(r * 1000.0, 6)
            if str(shape.Orientation) == "Reversed": data["is_internal"] = True
        if hasattr(geom, "Frame"):
            f = geom.Frame
            data["axis"] = [
                round(matrix[0][0]*f.DirZ.X + matrix[0][1]*f.DirZ.Y + matrix[0][2]*f.DirZ.Z, 6),
                round(matrix[1][0]*f.DirZ.X + matrix[1][1]*f.DirZ.Y + matrix[1][2]*f.DirZ.Z, 6),
                round(matrix[2][0]*f.DirZ.X + matrix[2][1]*f.DirZ.Y + matrix[2][2]*f.DirZ.Z, 6)
            ]
    except: pass
    return data

def extract_geometry():
    print("--- SCDM Universal Discovery (v4.61) ---")
    all_bodies_raw = []
    try: 
        root = GetRootPart()
        print(" - Active Root Part: " + root.Name)
        
        # 방식 1: GetDescendants (가장 강력함)
        try:
            desc_bodies = list(root.GetDescendants[IDesignBody]())
            for b in desc_bodies: all_bodies_raw.append(b)
        except: pass
        
        # 방식 2: 만약 방식 1이 실패하거나 부족하면 직접 순회
        if not all_bodies_raw:
            print(" - Fallback: Manual Traversal...")
            for body in root.Bodies: all_bodies_raw.append(body)
            for comp in root.Components:
                for body in comp.Template.Bodies: all_bodies_raw.append(body)
                
        # 중복 제거 (HashCode 기준)
        seen_hashes = set()
        unique_bodies = []
        for b in all_bodies_raw:
            h = b.GetHashCode()
            if h not in seen_hashes:
                unique_bodies.append(b)
                seen_hashes.add(h)
                
    except Exception as re:
        print(" - [ERROR] Discovery Failed: " + str(re))
        return [], [], "mm"
    
    print(" - Unique bodies found: {0}".format(len(unique_bodies)))
    final_data = []
    for i, body in enumerate(unique_bodies):
        b_name = "Unknown"
        try: b_name = body.Name
        except: pass
        
        # 좌표 행렬 (기본 Identity)
        matrix = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
        try:
            parent = body.ParentComponent
            if parent:
                t = parent.TransformToRoot
                matrix[0][3] = t.Translation.X * 1000.0
                matrix[1][3] = t.Translation.Y * 1000.0
                matrix[2][3] = t.Translation.Z * 1000.0
        except: pass
        
        vol = 0.0
        try: vol = body.Shape.Volume * 1e9
        except: pass
        
        bdata = {"body_index": i, "body_name": b_name, "volume": vol, "faces": []}
        for face in list(body.Faces):
            bdata["faces"].append(get_face_data(face, matrix))
        final_data.append(bdata)
        print("   [OK] Body {0}: '{1}' extracted.".format(i, b_name))
            
    return final_data, [], "mm"

try:
    results, warns, uinfo = extract_geometry()
    final = {"sub_device_name": "DEVICE", "units": "mm", "bodies": results}
    with open(OUTPUT_PATH, "w") as f: json.dump(final, f, indent=2)
    print("\n[FINISH] Universal extraction complete.")
except Exception as e: print("\n[FATAL] " + str(e))
