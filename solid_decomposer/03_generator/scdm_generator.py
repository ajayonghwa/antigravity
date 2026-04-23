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
            if strat == "OGRID":
                execution_calls += f"apply_ogrid('{body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
            elif strat == "CGRID":
                execution_calls += f"apply_cgrid('{body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
            elif strat == "RADIAL_OFFSET":
                execution_calls += f"apply_radial_offset('{body}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane('{body}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"

        script_template = f"""
# -*- coding: utf-8 -*-
import clr
import System
import math

def initialize_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        from SpaceClaim.Api.V22 import *
        from SpaceClaim.Api.V22.Modeler import *
        from SpaceClaim.Api.V22.Commands import *
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
    return [b for b in all_bodies if b.Name == target_name or b.Name.startswith(target_name + "_")]

def _get_safe_range(obj):
    for attr in ['Range', 'Box', 'BoundingBox', 'Extent']:
        if hasattr(obj, attr): return getattr(obj, attr)
    return None

def _get_target_cutter_comp(target_body_name):
    '''타겟 바디별 전용 커터 컴포넌트 생성'''
    root = GetRootPart()
    comp_name = "CUTTERS_FOR_" + target_body_name
    for comp in root.Components:
        if comp.Name == comp_name: return comp
    return Component.Create(root, comp_name)

def _create_cylindrical_cutter(target_body, origin_pt, direction, radius, name):
    try:
        root = GetRootPart()
        bbox = _get_safe_range(target_body)
        extrude_dist = 2.0
        if bbox:
            diag = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2)
            extrude_dist = max(diag * 3.0, 0.1)
        
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
        except: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
        
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
    print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, target_name))
    targets = get_matching_bodies(target_name)
    if not targets: return

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
            
            try:
                SplitBody.ByCutter(Selection.Create(target), Selection.Create(cutter_face), True, None)
                print("    [OK] Split Success")
            except: pass

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, target_name))
    targets = get_matching_bodies(target_name)
    if not targets: return
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            bbox = _get_safe_range(target)
            huge_radius = 5.0
            if bbox:
                huge_radius = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2) * 3.0
            
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
                try: 
                    SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool.Faces[0]), True, None)
                    print("    [OK] Split Success")
                except: pass
            design_curve.Delete()
        except: pass

def finalize():
    print(" --- Finished. Cutters preserved in specialized components. ---")
    try:
        from SpaceClaim.Api.V22.Commands import PartSharedTopology
        PartSharedTopology.Share(GetRootPart(), None)
    except: pass

# --- EXECUTION ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f:
            f.write(script_template)
        return output_path
