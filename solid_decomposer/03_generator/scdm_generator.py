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
            comp_creation_calls += f"create_body_component('{bname_b64}', {b_idx})\n"

        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body_idx = plan.get("body_index", 0)
            body = plan.get("body_name", "Unknown")
            body_b64 = base64.b64encode(body.encode('utf-8')).decode('ascii')
            if strat == "OGRID": execution_calls += f"apply_ogrid('{body_b64}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i}, {body_idx})\n"
            elif strat == "CGRID": execution_calls += f"apply_cgrid('{body_b64}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i}, {body_idx})\n"
            elif strat == "RADIAL_OFFSET": execution_calls += f"apply_radial_offset('{body_b64}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i}, {body_idx})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane('{body_b64}', {split['origin']}, {split['normal']}, '{strat}', {i}, {body_idx})\n"

        script_template = f"""# -*- coding: utf-8 -*-
import math
import base64
import re

BODY_COMP_MAP = {{}}

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
    # [v4.31] 분할 후 공백이나 괄호가 붙는 경우도 매칭되도록 강화
    pattern = re.compile(re.escape(target_name) + r"(_|\s|\(|$)")
    for b in all_bodies:
        if pattern.match(b.Name): matched.append(b)
    return matched

def create_body_component(name_b64, body_idx):
    global BODY_COMP_MAP
    root = GetRootPart()
    try: t_name = base64.b64decode(name_b64).decode('utf-8')
    except: t_name = name_b64
    safe_name = "".join(c for c in t_name if c.isalnum() or c == u"_")
    comp_name = "CUTTERS_FOR_{{0}}_{{1}}".format(safe_name, body_idx)
    target_comp = None
    for comp in root.Components:
        if comp.Name == comp_name:
            target_comp = comp
            break
    if not target_comp:
        try:
            target_part = Part.Create(root.Document, comp_name)
            target_comp = Component.Create(root, target_part)
        except: target_comp = None
    BODY_COMP_MAP[body_idx] = target_comp
    print(" - Created component for {{0}}".format(t_name))

def _move_body_to_comp(body, body_idx):
    global BODY_COMP_MAP
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return False
    try:
        # [v4.31] IComponent 객체에 직접 SetParent 시도
        body.SetParent(target_comp)
        return True
    except:
        try:
            # 실패 시 Copy/Delete 재시도 (Part 대상)
            body.Copy(target_comp.Template)
            body.Delete()
            return True
        except: return False

def _safe_split_multi(targets, cutter_face):
    if not targets: return False
    valid_targets = [t for t in targets if hasattr(t, "Shape") and t.Shape]
    if not valid_targets: return False
    try:
        sel = Selection.Create(valid_targets)
        res = SplitBody.ByCutter(sel, Selection.Create(cutter_face), True, None)
        return True
    except:
        try:
            SplitBody.Execute(Selection.Create(valid_targets), Selection.Create(cutter_face))
            return True
        except: return False

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    tname = base64.b64decode(body_b64).decode('utf-8')
    print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, tname))
    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])
    root = GetRootPart()
    try:
        bodies_before = list(root.GetDescendants[IDesignBody]())
        diag = 1.0
        r = getattr(targets[0].Shape, "Range", None)
        if r: diag = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2)
        extrude_dist = max(diag * 20.0, 2.0)
        shifted_origin = Point.Create(origin_pt.X - axis[0] * extrude_dist/2, origin_pt.Y - axis[1] * extrude_dist/2, origin_pt.Z - axis[2] * extrude_dist/2)
        frame = Frame.Create(shifted_origin, direction)
        circle = Circle.Create(frame, offset)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle))
        try: ExtrudeEdges.Execute(Selection.Create(design_curve), extrude_dist, ExtrudeEdgeOptions(), None)
        except: pass
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies:
            tool = new_bodies[0]
            tool.Name = "Cutter_OGrid_{{0}}".format(idx)
            cutter_face = tool.Faces[0]
            for f in tool.Faces:
                if "Cylinder" in f.Shape.Geometry.GetType().Name: cutter_face = f; break
            if _safe_split_multi(targets, cutter_face): print("    [OK] Multi-Split Success")
            _move_body_to_comp(tool, b_idx)
        design_curve.Delete()
    except Exception as e: print("    [ERROR] " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    tname = base64.b64decode(body_b64).decode('utf-8')
    print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, tname))
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()
    try:
        bodies_before = list(root.GetDescendants[IDesignBody]())
        circle_geom = Circle.Create(frame, 50.0) # 50미터
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
        Fill.Execute(Selection.Create(design_curve))
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies:
            tool = new_bodies[0]
            tool.Name = "Cutter_{{0}}_{{1}}".format(strategy, idx)
            if _safe_split_multi(targets, tool.Faces[0]): print("    [OK] Multi-Split Success")
            _move_body_to_comp(tool, b_idx)
        design_curve.Delete()
    except Exception as e: print("    [ERROR] " + str(e))

def finalize(): print(" --- Finished ---")
# --- INITIALIZATION ---
{comp_creation_calls}
# --- EXECUTION ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f: f.write(script_template)
        return output_path
