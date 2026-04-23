# -*- coding: utf-8 -*-
import os

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.output_dir = os.path.join(project_root, "04_scripts")
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir)
            except: self.output_dir = project_root

    def generate_script(self, plan_list, output_name="scdm_decomposition_script.py"):
        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body = plan.get("body_name", "Unknown")
            
            safe_body = body.replace("'", "\\'")
            
            if strat == "OGRID":
                execution_calls += f"apply_ogrid('{safe_body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
            elif strat == "CGRID":
                execution_calls += f"apply_cgrid('{safe_body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
            elif strat == "RADIAL_OFFSET":
                execution_calls += f"apply_radial_offset('{safe_body}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane('{safe_body}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"

        # [v4.18] 스페이스클레임 스크립트 에디터 순정 환경 복구
        # 불필요한 clr.AddReference 및 import 구문을 전면 제거하여 에디터 내장 기능(GetAllBodies 등)과의 충돌을 방지합니다.
        script_template = f"""# -*- coding: utf-8 -*-
import math

ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    try:
        # V22 에디터 환경 내장 메서드 우선
        for b in part.GetAllBodies(): body_list.append(b)
        return
    except: pass
    
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if comp.Template: get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(target_name):
    # 한글 비교를 위해 UTF-8 바이트 스트링을 유니코드로 안전하게 변환
    try:
        target_unicode = target_name.decode('utf-8')
    except:
        target_unicode = target_name
        
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for b in all_bodies:
        # b.Name은 .NET String이므로 파이썬의 unicode와 비교해야 함
        if b.Name == target_unicode or b.Name.startswith(target_unicode + u"_"):
            matched.append(b)
    return matched

def _get_target_cutter_comp(target_body_name):
    root = GetRootPart()
    try: t_name = target_body_name.decode('utf-8')
    except: t_name = target_body_name
    
    safe_name = "".join(c for c in t_name if c.isalnum() or c == u"_")
    comp_name = "CUTTERS_FOR_" + safe_name
    for comp in root.Components:
        if comp.Name == comp_name: return comp
    return Component.Create(root, comp_name)

def _safe_split(target_body, cutter_face):
    try:
        res = SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(cutter_face), True, None)
        if res.CreatedBodies.Count > 0: return True
    except: pass
    try:
        SplitBody.Execute(Selection.Create(target_body), Selection.Create(cutter_face))
        return True
    except: pass
    return False

def _create_cylindrical_cutter(target_body, origin_pt, direction, radius, name):
    try:
        root = GetRootPart()
        r = getattr(target_body.Shape, "Range", getattr(target_body, "Box", getattr(target_body, "BoundingBox", None)))
        extrude_dist = 2.0
        if r:
            diag = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2)
            extrude_dist = max(diag * 4.0, 0.1)
        
        shifted_origin = Point.Create(origin_pt.X - direction.X * extrude_dist/2, 
                                      origin_pt.Y - direction.Y * extrude_dist/2, 
                                      origin_pt.Z - direction.Z * extrude_dist/2)
        
        frame = Frame.Create(shifted_origin, direction)
        circle = Circle.Create(frame, radius)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle))
        
        sel = Selection.Create(design_curve)
        try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
        except: 
            try: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
            except: pass
        
        # 커터 찾기 (새로 생성된 바디)
        # 방금 만든 디자인 커브와 연관된 바디를 찾습니다.
        tool = None
        for b in root.Bodies:
            if getattr(b, 'Shape', None) and "Cylinder" in b.Shape.Geometry.GetType().Name:
                if b.Name.startswith("Solid") or b.Name.startswith("솔리드"):
                    # 매우 최근에 만들어진 바디로 추정
                    tool = b
                    
        # 만약 못 찾았으면 모든 바디 중 마지막 바디를 선택
        if not tool and root.Bodies.Count > 0:
            tool = root.Bodies[-1]
            
        design_curve.Delete()
        
        if tool:
            tool.Name = name
            tool.SetParent(_get_target_cutter_comp(target_body.Name))
            return tool
        return None
    except: return None

def apply_ogrid(target_name, center, axis, offset, idx):
    global ALL_CUTTERS
    try: print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, target_name.decode('utf-8')))
    except: print(" -> Step {{0}}: O-GRID".format(idx))
        
    targets = get_matching_bodies(target_name)
    if not targets:
        print("    [ERROR] Could not find target body")
        return

    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])

    for i, target in enumerate(targets):
        cutter_name = "Cutter_OGrid_Hole_{{0}}_{{1}}".format(idx, i)
        tool = _create_cylindrical_cutter(target, origin_pt, direction, offset, cutter_name)
        if tool:
            ALL_CUTTERS.append(tool)
            cutter_face = None
            for face in tool.Faces:
                if "Cylinder" in face.Shape.Geometry.GetType().Name:
                    cutter_face = face
                    break
            if not cutter_face: cutter_face = tool.Faces[0]
            
            if _safe_split(target, cutter_face):
                print("    [OK] Split Success")
            else:
                print("    [FAIL] Split failed")

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    try: print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, target_name.decode('utf-8')))
    except: print(" -> Step {{0}}: {{1}}".format(idx, strategy))
    
    targets = get_matching_bodies(target_name)
    if not targets:
        print("    [ERROR] Could not find target body")
        return
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            r = getattr(target.Shape, "Range", getattr(target, "Box", getattr(target, "BoundingBox", None)))
            huge_radius = 5.0
            if r:
                huge_radius = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2) * 4.0
            
            circle_geom = Circle.Create(frame, huge_radius)
            design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
            
            Fill.Execute(Selection.Create(design_curve))
            
            tool = None
            for b in root.Bodies:
                if getattr(b, 'Shape', None) and "Plane" in b.Shape.Geometry.GetType().Name:
                    if b.Name.startswith("Surface") or b.Name.startswith("서피스"):
                        tool = b
            if not tool and root.Bodies.Count > 0:
                tool = root.Bodies[-1]
            
            if tool:
                tool.Name = "Cutter_{{0}}_{{1}}_{{2}}".format(strategy, idx, i)
                tool.SetParent(_get_target_cutter_comp(target.Name))
                ALL_CUTTERS.append(tool)
                if _safe_split(target, tool.Faces[0]):
                    print("    [OK] Split Success")
                else:
                    print("    [FAIL] Split failed")
            design_curve.Delete()
        except: pass

def finalize():
    print(" --- Finished ---")

# --- EXECUTION ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        return output_path
