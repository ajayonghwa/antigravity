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
            
            # [v4.16] u"..." 유니코드 접두사 유지
            safe_body = body.replace("'", "\\'")
            
            if strat == "OGRID":
                execution_calls += f"apply_ogrid(u'{safe_body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
            elif strat == "CGRID":
                execution_calls += f"apply_cgrid(u'{safe_body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
            elif strat == "RADIAL_OFFSET":
                execution_calls += f"apply_radial_offset(u'{safe_body}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane(u'{safe_body}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"

        # [v4.17] 스페이스클레임 스크립트 에디터 환경에 맞는 와일드카드 임포트 복구
        # 불완전한 전역 변수 할당(SC_Point 등)으로 인한 초기화 실패를 방지
        script_template = f"""# -*- coding: utf-8 -*-
import clr
import System
import math

def initialize_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        from SpaceClaim.Api.V22 import *
        from SpaceClaim.Api.V22.Modeler import *
        try: from SpaceClaim.Api.V22.Commands import *
        except: pass
        return True
    except: return False

initialize_api()

ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if comp.Template: get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(target_name):
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for b in all_bodies:
        if b.Name == target_name or b.Name.startswith(target_name + u"_"):
            matched.append(b)
    return matched

def _get_safe_range(obj):
    for attr in ['Range', 'Box', 'BoundingBox', 'Extent']:
        if hasattr(obj, attr): return getattr(obj, attr)
    return None

def _get_target_cutter_comp(target_body_name):
    root = GetRootPart()
    safe_name = "".join(c for c in target_body_name if c.isalnum() or c == u"_")
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
        r = getattr(target_body.Shape, "Range", getattr(target_body, "Box", None))
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
        
        bodies_before = []
        get_all_bodies_recursive(root, bodies_before)
        
        sel = Selection.Create(design_curve)
        try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
        except: 
            try: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
            except: pass
        
        bodies_after = []
        get_all_bodies_recursive(root, bodies_after)
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        design_curve.Delete()
        
        if new_bodies:
            tool = new_bodies[0]
            tool.Name = name
            tool.SetParent(_get_target_cutter_comp(target_body.Name))
            return tool
        return None
    except: return None

def apply_ogrid(target_name, center, axis, offset, idx):
    global ALL_CUTTERS
    try: print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, target_name))
    except: print(" -> Step {{0}}: O-GRID".format(idx))
        
    targets = get_matching_bodies(target_name)
    if not targets:
        try: print("    [ERROR] Could not find target body: " + target_name)
        except: print("    [ERROR] Could not find target body")
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
                try: print("    [FAIL] Split failed for " + target.Name)
                except: print("    [FAIL] Split failed")

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    try: print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, target_name))
    except: print(" -> Step {{0}}: {{1}}".format(idx, strategy))
    
    targets = get_matching_bodies(target_name)
    if not targets:
        try: print("    [ERROR] Could not find target body: " + target_name)
        except: print("    [ERROR] Could not find target body")
        return
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            r = getattr(target.Shape, "Range", getattr(target, "Box", None))
            huge_radius = 5.0
            if r:
                huge_radius = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2) * 4.0
            
            circle_geom = Circle.Create(frame, huge_radius)
            design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
            
            bodies_before = []
            get_all_bodies_recursive(root, bodies_before)
            Fill.Execute(Selection.Create(design_curve))
            
            bodies_after = []
            get_all_bodies_recursive(root, bodies_after)
            new_bodies = [b for b in bodies_after if b not in bodies_before]
            
            if new_bodies:
                tool = new_bodies[0]
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
    try:
        from SpaceClaim.Api.V22.Commands import PartSharedTopology
        PartSharedTopology.Share(GetRootPart(), None)
    except: pass

# --- EXECUTION ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        return output_path
