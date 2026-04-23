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

        script_template = f"""# -*- coding: utf-8 -*-
import math

ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    try:
        # GetDescendants is the most robust way in V22
        for b in part.GetDescendants[IDesignBody]():
            body_list.append(b)
        return
    except: pass
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if hasattr(comp, "Template") and comp.Template:
            get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(target_name):
    try: target_unicode = target_name.decode('utf-8')
    except: target_unicode = target_name
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for b in all_bodies:
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
    try:
        new_part = Part.Create(root.Document, comp_name)
        return Component.Create(root, new_part)
    except: return root

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

def apply_ogrid(target_name, center, axis, offset, idx):
    print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, target_name))
    targets = get_matching_bodies(target_name)
    if not targets: return

    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            # [무적 로직] 실행 전 바디 목록 캡처
            bodies_before = list(root.GetDescendants[IDesignBody]())
            
            r = getattr(target.Shape, "Range", getattr(target, "Box", getattr(target, "BoundingBox", None)))
            extrude_dist = 2.0
            if r:
                diag = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2)
                extrude_dist = max(diag * 4.0, 0.1)
            
            shifted_origin = Point.Create(origin_pt.X - axis[0] * extrude_dist/2, 
                                          origin_pt.Y - axis[1] * extrude_dist/2, 
                                          origin_pt.Z - axis[2] * extrude_dist/2)
            frame = Frame.Create(shifted_origin, direction)
            circle = Circle.Create(frame, offset)
            design_curve = DesignCurve.Create(root, CurveSegment.Create(circle))
            
            # 실린더 생성
            sel = Selection.Create(design_curve)
            try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
            except: 
                try: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
                except: pass
            
            # 새 바디 찾기
            bodies_after = list(root.GetDescendants[IDesignBody]())
            new_bodies = [b for b in bodies_after if b not in bodies_before]
            
            if new_bodies:
                tool = new_bodies[0]
                tool.Name = "Cutter_OGrid_{{0}}_{{1}}".format(idx, i)
                
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
                
                # 컴포넌트 이동
                try: tool.SetParent(_get_target_cutter_comp(target.Name))
                except: pass
            
            design_curve.Delete()
        except Exception as e: print("    [ERROR] " + str(e))

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, target_name))
    targets = get_matching_bodies(target_name)
    if not targets: return
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            bodies_before = list(root.GetDescendants[IDesignBody]())
            
            r = getattr(target.Shape, "Range", getattr(target, "Box", getattr(target, "BoundingBox", None)))
            huge_radius = 5.0
            if r:
                huge_radius = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2) * 4.0
            
            circle_geom = Circle.Create(frame, huge_radius)
            design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
            Fill.Execute(Selection.Create(design_curve))
            
            bodies_after = list(root.GetDescendants[IDesignBody]())
            new_bodies = [b for b in bodies_after if b not in bodies_before]
            
            if new_bodies:
                tool = new_bodies[0]
                tool.Name = "Cutter_{{0}}_{{1}}_{{2}}".format(strategy, idx, i)
                
                if _safe_split(target, tool.Faces[0]):
                    print("    [OK] Split Success")
                else:
                    print("    [FAIL] Split failed")
                
                try: tool.SetParent(_get_target_cutter_comp(target.Name))
                except: pass
                
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
