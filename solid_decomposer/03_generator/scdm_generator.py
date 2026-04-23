# -*- coding: utf-8 -*-
import os
import base64

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.output_dir = os.path.join(project_root, "04_scripts")
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir)
            except: self.output_dir = project_root

    def generate_script(self, plan_list, output_name="scdm_decomposition_script.py"):
        unique_body_indices = sorted(list(set([p.get("body_index", 0) for p in plan_list])))
        body_index_to_name = {}
        for p in plan_list: body_index_to_name[p.get("body_index", 0)] = p.get("body_name", "Unknown")

        comp_creation_calls = ""
        for b_idx in unique_body_indices:
            bname = body_index_to_name[b_idx]
            bname_b64 = base64.b64encode(bname.encode('utf-8')).decode('ascii')
            comp_creation_calls += "create_body_component('{0}', {1})\n".format(bname_b64, b_idx)

        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body_idx = plan.get("body_index", 0)
            body = plan.get("body_name", "Unknown")
            body_b64 = base64.b64encode(body.encode('utf-8')).decode('ascii')
            if strat == "OGRID":
                execution_calls += "apply_ogrid('{0}', {1}, {2}, {3}, {4}, {5})\n".format(body_b64, plan['center'], plan['axis'], plan['core_offset'], i, body_idx)
            elif strat == "CGRID":
                execution_calls += "apply_cgrid('{0}', {1}, {2}, {3}, {4}, {5}, {6})\n".format(body_b64, plan['center'], plan['axis'], plan['core_offset'], plan.get('wall_direction', [0,0,1]), i, body_idx)
            elif strat == "RADIAL_OFFSET":
                execution_calls += "apply_radial_offset('{0}', {1}, {2}, {3}, {4}, {5})\n".format(body_b64, plan['center'], plan['axis'], plan['split_radius'], i, body_idx)
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += "apply_split_plane('{0}', {1}, {2}, '{3}', {4}, {5})\n".format(body_b64, split['origin'], split['normal'], strat, i, body_idx)

        # [v4.47] f-string을 사용하지 않고 문자열 템플릿 사용 (중괄호 에러 방지)
        template = """# -*- coding: utf-8 -*-
import math
import base64
import re
import clr

# [v4.47] 명시적 V22 참조 및 전역 임포트
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
    from SpaceClaim.Api.V22.Commands import *
except: pass

BODY_COMP_MAP = {}

def get_all_bodies_recursive(part, body_list):
    try:
        for b in part.GetDescendants[IDesignBody](): body_list.append(b)
        return
    except: pass
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if hasattr(comp, "Template") and comp.Template: get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(body_b64):
    try: target_name = base64.b64decode(body_b64).decode('utf-8')
    except: target_name = body_b64
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    pattern = re.compile(re.escape(target_name) + r"(_|\\s|\\(|\\d|$)")
    for b in all_bodies:
        if pattern.match(b.Name): matched.append(b)
    return matched

def create_body_component(name_b64, body_idx):
    global BODY_COMP_MAP
    root = GetRootPart()
    try: t_name = base64.b64decode(name_b64).decode('utf-8')
    except: t_name = name_b64
    safe_name = "".join(c for c in t_name if c.isalnum() or c == "_")
    comp_name = "CUTTERS_FOR_{0}_{1}".format(safe_name, body_idx)
    target_comp = None
    for comp in root.Components:
        if comp.Name == comp_name: target_comp = comp; break
    if not target_comp:
        try:
            target_part = Part.Create(root.Document, comp_name)
            target_comp = Component.Create(root, target_part)
        except: pass
    BODY_COMP_MAP[body_idx] = target_comp

def _move_body_to_comp(body, body_idx):
    global BODY_COMP_MAP
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return False
    try:
        # 매뉴얼 지침: ComponentHelper 우선 사용
        ComponentHelper.MoveBodiesToComponent(Selection.Create(body), target_comp)
        return True
    except:
        try:
            MoveToComponent.Execute(Selection.Create(body), target_comp, True, None)
            return True
        except:
            try:
                # 매뉴얼 12번 지침: Copy/Delete
                new_shape = body.Shape.Copy()
                DesignBody.Create(target_comp.Template, "Cutter_Copy", new_shape)
                body.Delete()
                return True
            except: return False

def _get_dynamic_cutter_radius():
    try:
        r = GetRootPart().Range
        diag = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2)
        return diag * 2.0
    except: return 100.0

def _safe_split_multi(targets, cutter_face):
    if not targets: return False
    valid_targets = [t for t in targets if hasattr(t, "Shape") and t.Shape]
    if not valid_targets: return False
    try:
        # 매뉴얼 2번 지침: ByCutter (4인자)
        SplitBody.ByCutter(Selection.Create(valid_targets), Selection.Create(cutter_face), True, None)
        return True
    except:
        try: SplitBody.Execute(Selection.Create(valid_targets), Selection.Create(cutter_face), True, None)
        except: return False

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    tname = base64.b64decode(body_b64).decode('utf-8')
    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])
    root = GetRootPart()
    try:
        bodies_before = list(root.GetDescendants[IDesignBody]())
        circle = Circle.Create(Frame.Create(origin_pt, direction), offset)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle))
        try: ExtrudeEdges.ByDistance(Selection.Create(design_curve), 20.0, ExtrudeEdgeOptions(), None)
        except: ExtrudeEdges.Execute(Selection.Create(design_curve), 20.0, ExtrudeEdgeOptions(), None)
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies:
            tool = new_bodies[0]
            if _safe_split_multi(targets, tool.Faces[0]): print("    [OK] Split O-GRID")
            _move_body_to_comp(tool, b_idx)
        design_curve.Delete()
    except Exception as e: print("    [ERROR] OGRID failed: " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    tname = base64.b64decode(body_b64).decode('utf-8')
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    root = GetRootPart()
    try:
        bodies_before = list(root.GetDescendants[IDesignBody]())
        radius = _get_dynamic_cutter_radius()
        circle_geom = Circle.Create(Frame.Create(origin, normal), radius)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
        try: Fill.By(Selection.Create(design_curve))
        except: Fill.Execute(Selection.Create(design_curve), None, FillOptions(), None)
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies:
            tool = new_bodies[0]
            if _safe_split_multi(targets, tool.Faces[0]): print("    [OK] Split " + strategy)
            _move_body_to_comp(tool, b_idx)
        design_curve.Delete()
    except Exception as e: print("    [ERROR] SplitPlane failed: " + str(e))

def finalize(): print(" --- Finished ---")
# --- INITIALIZATION ---
REPLACE_COMP_CREATION
# --- EXECUTION ---
REPLACE_EXECUTION
finalize()
"""
        script_content = template.replace("REPLACE_COMP_CREATION", comp_creation_calls)
        script_content = script_content.replace("REPLACE_EXECUTION", execution_calls)
        
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f: f.write(script_content)
        return output_path
