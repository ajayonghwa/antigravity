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
        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body_idx = plan.get("body_index", i)
            body = plan.get("body_name", "Unknown")
            body_b64 = base64.b64encode(body.encode('utf-8')).decode('ascii')
            
            if strat == "OGRID":
                execution_calls += f"apply_ogrid('{body_b64}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i}, {body_idx})\n"
            elif strat == "CGRID":
                execution_calls += f"apply_cgrid('{body_b64}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i}, {body_idx})\n"
            elif strat == "RADIAL_OFFSET":
                execution_calls += f"apply_radial_offset('{body_b64}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i}, {body_idx})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane('{body_b64}', {split['origin']}, {split['normal']}, '{strat}', {i}, {body_idx})\n"

        script_template = f"""# -*- coding: utf-8 -*-
import math
import base64

ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    try:
        for b in part.GetDescendants[IDesignBody](): body_list.append(b)
        return
    except: pass
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if hasattr(comp, "Template") and comp.Template:
            get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(body_b64):
    try: target_name = base64.b64decode(body_b64).decode('utf-8')
    except: target_name = body_b64
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for b in all_bodies:
        if b.Name == target_name or b.Name.startswith(target_name + u"_"):
            matched.append(b)
    return matched

def _move_body_to_comp(body, target_body_name, body_idx):
    # [v4.27] 바디별 고유 컴포넌트 생성 및 Copy/Delete 방식으로 이동 보장
    root = GetRootPart()
    try: t_name = target_body_name.decode('utf-8')
    except: t_name = target_body_name
    safe_name = "".join(c for c in t_name if c.isalnum() or c == u"_")
    comp_name = "CUTTERS_FOR_{{0}}_{{1}}".format(safe_name, body_idx)
    
    target_part = None
    for comp in root.Components:
        if comp.Name == comp_name:
            target_part = comp.Template
            break
            
    if not target_part:
        try:
            target_part = Part.Create(root.Document, comp_name)
            Component.Create(root, target_part)
        except: target_part = root
        
    try:
        # 스페이스클레임에서 바디 이동은 Copy(Part) -> Delete()가 가장 확실합니다.
        body.Copy(target_part)
        body.Delete()
        return True
    except: return False

def _safe_split_multi(targets, cutter_face):
    if not targets: return False
    try:
        sel = Selection.Create(targets)
        res = SplitBody.ByCutter(sel, Selection.Create(cutter_face), True, None)
        if res.CreatedBodies.Count > 0: return True
    except: pass
    try:
        SplitBody.Execute(Selection.Create(targets), Selection.Create(cutter_face))
        return True
    except: pass
    return False

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
        diag = 2.0
        r = getattr(targets[0].Shape, "Range", getattr(targets[0], "Box", getattr(targets[0], "BoundingBox", None)))
        if r: diag = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2)
        extrude_dist = max(diag * 10.0, 0.5)
        
        shifted_origin = Point.Create(origin_pt.X - axis[0] * extrude_dist/2, 
                                      origin_pt.Y - axis[1] * extrude_dist/2, 
                                      origin_pt.Z - axis[2] * extrude_dist/2)
        frame = Frame.Create(shifted_origin, direction)
        circle = Circle.Create(frame, offset)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle))
        
        try: ExtrudeEdges.Execute(Selection.Create(design_curve), extrude_dist, ExtrudeEdgeOptions(), None)
        except: 
            try: ExtrudeEdges.Execute(Selection.Create(design_curve), Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
            except: pass
        
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies:
            tool = new_bodies[0]
            tool.Name = "Cutter_OGrid_{{0}}".format(idx)
            cutter_face = tool.Faces[0]
            for f in tool.Faces:
                if "Cylinder" in f.Shape.Geometry.GetType().Name:
                    cutter_face = f
                    break
            if _safe_split_multi(targets, cutter_face): print("    [OK] Multi-Split Success")
            else: print("    [FAIL] Multi-Split failed")
            _move_body_to_comp(tool, tname, b_idx)
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
        huge_radius = 10.0
        circle_geom = Circle.Create(frame, huge_radius)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
        Fill.Execute(Selection.Create(design_curve))
        
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies:
            tool = new_bodies[0]
            tool.Name = "Cutter_{{0}}_{{1}}".format(strategy, idx)
            if _safe_split_multi(targets, tool.Faces[0]): print("    [OK] Multi-Split Success")
            else: print("    [FAIL] Multi-Split failed")
            _move_body_to_comp(tool, tname, b_idx)
        design_curve.Delete()
    except Exception as e: print("    [ERROR] " + str(e))

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
