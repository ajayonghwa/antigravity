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
            body = plan.get("body_name", "Unknown")
            
            # [v4.24] 한글 깨짐을 100% 방지하기 위해 바디 이름을 Base64로 인코딩하여 전달합니다.
            body_b64 = base64.b64encode(body.encode('utf-8')).decode('ascii')
            
            if strat == "OGRID":
                execution_calls += f"apply_ogrid('{body_b64}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
            elif strat == "CGRID":
                execution_calls += f"apply_cgrid('{body_b64}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
            elif strat == "RADIAL_OFFSET":
                execution_calls += f"apply_radial_offset('{body_b64}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane('{body_b64}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"

        script_template = f"""# -*- coding: utf-8 -*-
import math
import base64

ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    try:
        for b in part.GetAllBodies(): body_list.append(b)
        return
    except: pass
    try:
        for b in part.GetDescendants[IDesignBody](): body_list.append(b)
        return
    except: pass
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if hasattr(comp, "Template") and comp.Template:
            get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(body_b64):
    # Base64 디코딩으로 한글 깨짐 방지
    try:
        target_name = base64.b64decode(body_b64).decode('utf-8')
    except:
        target_name = body_b64
        
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for b in all_bodies:
        if b.Name == target_name or b.Name.startswith(target_name + u"_"):
            matched.append(b)
    return matched

def _get_target_cutter_comp(target_body_name):
    root = GetRootPart()
    safe_name = "".join(c for c in target_body_name if c.isalnum() or c == u"_")
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

def apply_ogrid(body_b64, center, axis, offset, idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    
    # 디코딩된 이름으로 로그 출력
    tname = base64.b64decode(body_b64).decode('utf-8')
    print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, tname))

    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
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
            
            sel = Selection.Create(design_curve)
            try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
            except: 
                try: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
                except: pass
            
            bodies_after = list(root.GetDescendants[IDesignBody]())
            new_bodies = [b for b in bodies_after if b not in bodies_before]
            
            if new_bodies:
                tool = new_bodies[0]
                tool.Name = "Cutter_OGrid_{{0}}_{{1}}".format(idx, i)
                cutter_face = tool.Faces[0]
                for face in tool.Faces:
                    if "Cylinder" in face.Shape.Geometry.GetType().Name:
                        cutter_face = face
                        break
                
                if _safe_split(target, cutter_face):
                    print("    [OK] Split Success")
                else:
                    print("    [FAIL] Split failed")
                
                try: tool.SetParent(_get_target_cutter_comp(target.Name))
                except: pass
            design_curve.Delete()
        except Exception as e: print("    [ERROR] " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    
    tname = base64.b64decode(body_b64).decode('utf-8')
    print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, tname))
    
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
