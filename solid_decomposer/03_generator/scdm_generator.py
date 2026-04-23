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

def initialize_api():
    try:
        clr.AddReference("SpaceClaim.Api.V22")
        from SpaceClaim.Api.V22 import *
        from SpaceClaim.Api.V22.Modeler import *
        from SpaceClaim.Api.V22.Commands import *
        return True
    except: return False

initialize_api()

# 전역 커터 관리
if 'ALL_CUTTERS' not in globals(): ALL_CUTTERS = []
CUTTER_COMP = None

def get_all_bodies_recursive(part, body_list):
    for body in part.Bodies: body_list.append(body)
    for comp in part.Components:
        if comp.Template: get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(target_name):
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    # 이름이 정확히 일치하거나, 분할되어 접미사가 붙은 바디들 수집
    return [b for b in all_bodies if b.Name == target_name or b.Name.startswith(target_name + "_")]

def _get_safe_range(obj):
    for attr in ['Range', 'Box', 'BoundingBox', 'Extent']:
        if hasattr(obj, attr): return getattr(obj, attr)
    return None

def _get_cutter_comp():
    '''커터들을 모아둘 전용 컴포넌트 생성/반환'''
    global CUTTER_COMP
    if CUTTER_COMP: return CUTTER_COMP
    root = GetRootPart()
    # 기존에 있으면 사용, 없으면 생성
    for comp in root.Components:
        if comp.Name == "AUTO_CUTTERS":
            CUTTER_COMP = comp
            return CUTTER_COMP
    CUTTER_COMP = Component.Create(root, "AUTO_CUTTERS")
    return CUTTER_COMP

def _move_to_cutter_comp(body):
    '''바디를 커터 컴포넌트로 이동'''
    try:
        comp = _get_cutter_comp()
        body.SetParent(comp)
    except: pass

def _create_cylindrical_cutter(target_body, origin_pt, direction, radius):
    try:
        root = GetRootPart()
        bbox = _get_safe_range(target_body)
        extrude_dist = 1.0
        if bbox:
            diag = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2)
            extrude_dist = diag * 2.5 # 더 넉넉하게
        
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
            _move_to_cutter_comp(tool)
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
        tool = _create_cylindrical_cutter(target, origin_pt, direction, offset)
        if tool:
            tool.Name = "Cutter_OGrid_" + str(idx) + "_" + str(i)
            ALL_CUTTERS.append(tool)
            try:
                # 겹침 방지를 위해 약간의 안정 시간(옵션) 혹은 즉시 분할
                res = SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool.Faces[0]), True, None)
                print("    [OK] Split Success")
            except Exception as e:
                print("    [SKIP] Unable to split: " + str(e))

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
            huge_radius = 2.0
            if bbox:
                huge_radius = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2) * 2.0
            
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
                tool.Name = "Cutter_Plane_" + strategy + "_" + str(idx) + "_" + str(i)
                _move_to_cutter_comp(tool)
                ALL_CUTTERS.append(tool)
                try: 
                    SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool.Faces[0]), True, None)
                    print("    [OK] Split Success")
                except: print("    [SKIP] Unable to split")
            design_curve.Delete()
        except: pass

def finalize():
    print(" -> Workflow Finished. 'AUTO_CUTTERS' component contains all used tools.")
    print(" -> If any split skipped, please manually use the cutters and delete them.")
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
