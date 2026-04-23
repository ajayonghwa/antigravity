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
        import SpaceClaim.Api.V22 as scapi
        global SC_Point, SC_Direction, SC_Frame, SC_Circle, SC_DesignCurve, SC_CurveSegment, SC_Selection, SC_SplitBody, SC_Component, SC_Fill, SC_ExtrudeEdges, SC_ExtrudeEdgeOptions
        SC_Point = scapi.Point
        SC_Direction = scapi.Direction
        SC_Frame = scapi.Frame
        SC_Circle = scapi.Circle
        SC_DesignCurve = scapi.DesignCurve
        SC_CurveSegment = scapi.CurveSegment
        SC_Selection = scapi.Selection
        SC_SplitBody = scapi.SplitBody
        SC_Component = scapi.Component
        SC_Fill = scapi.Fill
        SC_ExtrudeEdges = scapi.Modeler.ExtrudeEdges
        SC_ExtrudeEdgeOptions = scapi.Modeler.ExtrudeEdgeOptions
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
    root = GetRootPart()
    comp_name = "CUTTERS_FOR_" + target_body_name.split("_")[-1]
    for comp in root.Components:
        if comp.Name == comp_name: return comp
    return SC_Component.Create(root, comp_name)

def _safe_split(target_body, cutter_face):
    try:
        res = SC_SplitBody.ByCutter(SC_Selection.Create(target_body), SC_Selection.Create(cutter_face), True, None)
        if res.CreatedBodies.Count > 0: return True
    except: pass
    try:
        SC_SplitBody.Execute(SC_Selection.Create(target_body), SC_Selection.Create(cutter_face))
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
        
        shifted_origin = SC_Point.Create(origin_pt.X - direction.X * extrude_dist/2, 
                                         origin_pt.Y - direction.Y * extrude_dist/2, 
                                         origin_pt.Z - direction.Z * extrude_dist/2)
        
        frame = SC_Frame.Create(shifted_origin, direction)
        circle = SC_Circle.Create(frame, radius)
        design_curve = SC_DesignCurve.Create(root, SC_CurveSegment.Create(circle))
        
        bodies_before = []
        get_all_bodies_recursive(root, bodies_before)
        
        sel = SC_Selection.Create(design_curve)
        try: SC_ExtrudeEdges.Execute(sel, extrude_dist, SC_ExtrudeEdgeOptions(), None)
        except: SC_ExtrudeEdges.Execute(sel, SC_Selection.Create(direction), extrude_dist, SC_ExtrudeEdgeOptions(), None)
        
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

    origin_pt = SC_Point.Create(center[0], center[1], center[2])
    direction = SC_Direction.Create(axis[0], axis[1], axis[2])

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
                print("    [FAIL] Split failed for {{0}}".format(target.Name))

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, target_name))
    targets = get_matching_bodies(target_name)
    if not targets: return
    
    origin = SC_Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = SC_Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = SC_Frame.Create(origin, normal)
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            r = getattr(target.Shape, "Range", getattr(target, "Box", None))
            huge_radius = 5.0
            if r:
                huge_radius = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2) * 4.0
            
            circle_geom = SC_Circle.Create(frame, huge_radius)
            design_curve = SC_DesignCurve.Create(root, SC_CurveSegment.Create(circle_geom))
            
            bodies_before = []
            get_all_bodies_recursive(root, bodies_before)
            SC_Fill.Execute(SC_Selection.Create(design_curve))
            
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
        with open(output_path, "w") as f:
            f.write(script_template)
        return output_path
