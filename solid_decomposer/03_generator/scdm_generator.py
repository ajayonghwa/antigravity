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
        print(f"\n[Generating Script: {output_name}]")
        print(f" - Total plans to process: {len(plan_list)}")
        
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body = plan.get("body_name", "Unknown")
            
            if strat == "OGRID":
                call = f"apply_ogrid('{body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
                execution_calls += call
            elif strat == "CGRID":
                call = f"apply_cgrid('{body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
                execution_calls += call
            elif strat == "RADIAL_OFFSET":
                call = f"apply_radial_offset('{body}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
                execution_calls += call
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                call = f"apply_split_plane('{body}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"
                execution_calls += call

        script_template = f"""
# -*- coding: utf-8 -*-
import clr
import System
import math

# [1] API 로드 및 참조
def initialize_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        from SpaceClaim.Api.V22 import *
        from SpaceClaim.Api.V22.Modeler import *
        from SpaceClaim.Api.V22.Commands import *
        return True
    except:
        return False

initialize_api()

# 전역 커터 목록
if 'ALL_CUTTERS' not in globals():
    ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    '''모든 컴포넌트를 탐색하여 바디 수집'''
    for body in part.Bodies:
        body_list.append(body)
    for comp in part.Components:
        if comp.Template:
            get_all_bodies_recursive(comp.Template, body_list)

def make_all_bodies_independent():
    try:
        root = GetRootPart()
        all_bodies = []
        get_all_bodies_recursive(root, all_bodies)
        for body in all_bodies:
            try:
                shape_copy = body.Shape.Copy()
                new_body = DesignBody.Create(root, body.Name + "_indep", shape_copy)
                body.Delete()
            except: pass
    except: pass

def get_matching_bodies(target_name):
    '''이름이 정확히 일치하는 바디 탐색'''
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = [b for b in all_bodies if b.Name == target_name]
    return matched

def _create_cylindrical_cutter(origin_pt, direction, radius):
    '''원통형 커터 생성 (V22 최적화)'''
    try:
        root = GetRootPart()
        bbox = root.Range
        diag = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2)
        extrude_dist = max(diag * 1.5, 0.1)
        
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
        
        return new_bodies[0] if new_bodies else None
    except Exception as e:
        print("Cutter Creation Error: " + str(e))
        return None

def apply_ogrid(target_name, center, axis, offset, idx):
    global ALL_CUTTERS
    print(" -> Step {{0}}: O-GRID splitting for {{1}}".format(idx, target_name))
    
    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])
    
    targets = get_matching_bodies(target_name)
    if not targets:
        print("    !! Body not found: {{0}}".format(target_name))
        return

    for i, target in enumerate(targets):
        tool = _create_cylindrical_cutter(origin_pt, direction, offset)
        if tool:
            tool.Name = "Cutter_OGrid_" + str(idx)
            ALL_CUTTERS.append(tool)
            try:
                SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool.Faces[0]), True, None)
                print("    [OK] Split successful.")
            except Exception as e:
                print("    [FAIL] Split failed: " + str(e))

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    print(" -> Step {{0}}: {{1}} splitting for {{2}}".format(idx, strategy, target_name))
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()
    
    try:
        bbox = root.Range
        huge_radius = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2) * 1.5
        
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
            tool.Name = "Cutter_Plane_" + str(idx)
            ALL_CUTTERS.append(tool)
            targets = get_matching_bodies(target_name)
            for target in targets:
                try: 
                    SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool.Faces[0]), True, None)
                    print("    [OK] Split successful.")
                except Exception as e:
                    print("    [FAIL] Split failed: " + str(e))
        
        design_curve.Delete()
    except Exception as e:
        print("    [ERROR] Plane split error: " + str(e))

def finalize():
    global ALL_CUTTERS
    print(" -> Finalizing: Cleaning cutters and sharing topology...")
    for cutter in ALL_CUTTERS:
        try: cutter.Delete()
        except: pass
    try:
        from SpaceClaim.Api.V22.Commands import PartSharedTopology
        PartSharedTopology.Share(GetRootPart(), None)
    except: pass
    print(" --- Decomposition Workflow Finished ---")

# --- EXECUTION ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f:
            f.write(script_template)
        return output_path
