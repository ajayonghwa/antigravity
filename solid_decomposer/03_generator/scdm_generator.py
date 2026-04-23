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
                print(f"   -> Added O-GRID split for {body}")
            elif strat == "CGRID":
                call = f"apply_cgrid('{body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
                execution_calls += call
                print(f"   -> Added C-GRID split for {body}")
            elif strat == "RADIAL_OFFSET":
                call = f"apply_radial_offset('{body}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
                execution_calls += call
                print(f"   -> Added RADIAL_OFFSET split for {body}")
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                call = f"apply_split_plane('{body}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"
                execution_calls += call
                print(f"   -> Added {strat} split for {body}")
            else:
                print(f"   !! Warning: Unknown strategy '{strat}' skipped.")

        script_template = f"""
# -*- coding: utf-8 -*-
import clr
import System
import math

# 스페이스클레임 API 로드
def initialize_api():
    for v in range(22, 16, -1):
        try:
            ref = "SpaceClaim.Api.V" + str(v)
            clr.AddReference(ref)
            exec("from SpaceClaim.Api.V" + str(v) + " import *")
            exec("from SpaceClaim.Api.V" + str(v) + ".Modeler import *")
            exec("from SpaceClaim.Api.V" + str(v) + ".Commands import *")
            return True
        except: pass
    return False

initialize_api()

# 전역 커터 목록 초기화
if 'ALL_CUTTERS' not in globals():
    ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    '''모든 컴포넌트를 뒤져서 바디를 수집'''
    for body in part.Bodies:
        body_list.append(body)
    for comp in part.Components:
        if comp.Template:
            get_all_bodies_recursive(comp.Template, body_list)

def make_all_bodies_independent():
    '''패턴/인스턴스로 공유된 바디를 모두 독립화'''
    try:
        root = GetRootPart()
        all_bodies = []
        get_all_bodies_recursive(root, all_bodies)
        for body in all_bodies:
            try:
                # 바디 복사 후 원본 삭제 방식의 독립화
                shape_copy = body.Shape.Copy()
                new_body = DesignBody.Create(root, body.Name + "_indep", shape_copy)
                body.Delete()
            except: pass
    except Exception as e:
        print("Pattern independence failed: " + str(e))

def get_matching_bodies(target_base):
    '''이름 기반 3단계 매칭'''
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for body in all_bodies:
        b_name = body.Name
        if b_name == target_base or b_name.startswith(target_base + " "):
            matched.append(body)
    return matched

def _create_cylindrical_cutter(origin_pt, direction, radius):
    '''동적 스케일링이 적용된 원통형 커터 생성'''
    try:
        bbox = GetRootPart().Range
        diag = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2)
        extrude_dist = max(diag * 1.5, 0.1)
    except:
        extrude_dist = 5.0
        
    shifted_origin = Point.Create(origin_pt.X - direction.X * extrude_dist/2, 
                                  origin_pt.Y - direction.Y * extrude_dist/2, 
                                  origin_pt.Z - direction.Z * extrude_dist/2)
    
    frame = Frame.Create(shifted_origin, direction)
    circle = Circle.Create(frame, radius)
    design_curve = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle))
    
    tool_body = None
    try:
        bodies_before = list(GetRootPart().GetAllBodies())
        sel = Selection.Create(design_curve)
        try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
        except: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
        
        bodies_after = list(GetRootPart().GetAllBodies())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        if new_bodies: tool_body = new_bodies[0]
    except: pass
    
    design_curve.Delete()
    return tool_body

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, idx):
    global ALL_CUTTERS
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    
    targets = get_matching_bodies(target_full_name)
    for i, target_body in enumerate(targets):
        tool_body = _create_cylindrical_cutter(origin_pt, direction, core_offset)
        if tool_body:
            tool_body.Name = "Cutter_OGrid_" + str(idx) + "_" + str(i)
            ALL_CUTTERS.append(tool_body)
            try: SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True, None)
            except: pass

def apply_radial_offset(target_full_name, center_list, axis_list, split_radius, idx):
    global ALL_CUTTERS
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    
    targets = get_matching_bodies(target_full_name)
    for i, target_body in enumerate(targets):
        tool_body = _create_cylindrical_cutter(origin_pt, direction, split_radius)
        if tool_body:
            tool_body.Name = "Cutter_Radial_" + str(idx) + "_" + str(i)
            ALL_CUTTERS.append(tool_body)
            try: SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True, None)
            except: pass

def apply_cgrid(target_full_name, center_list, axis_list, core_offset, wall_dir, idx):
    apply_ogrid(target_full_name, center_list, axis_list, core_offset, idx)

def apply_split_plane(target_full_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    
    try:
        bbox = GetRootPart().Range
        diag = math.sqrt((bbox.Max.X - bbox.Min.X)**2 + (bbox.Max.Y - bbox.Min.Y)**2 + (bbox.Max.Z - bbox.Min.Z)**2)
        huge_radius = max(diag * 1.5, 0.1)
            
        circle_geom = Circle.Create(frame, huge_radius)
        design_curve = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle_geom))
        
        bodies_before = list(GetRootPart().GetAllBodies())
        try: Fill.Execute(Selection.Create(design_curve), None)
        except: Fill.Execute(Selection.Create(design_curve))
            
        bodies_after = list(GetRootPart().GetAllBodies())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        
        if new_bodies:
            tool_body = new_bodies[0]
            tool_body.Name = "Cutter_Surface_" + strategy + "_" + str(idx)
            ALL_CUTTERS.append(tool_body)
            
            targets = get_matching_bodies(target_full_name)
            for target in targets:
                try: SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool_body.Faces[0]), True, None)
                except: pass
        
        design_curve.Delete()
    except Exception as e:
        print(strategy + " split error: " + str(e))

def finalize():
    global ALL_CUTTERS
    if ALL_CUTTERS:
        try:
            for cutter in ALL_CUTTERS:
                try: cutter.Delete()
                except: pass
            PartSharedTopology.Share(GetRootPart(), None)
        except: pass

# --- Execution ---
# make_all_bodies_independent() # 필요 시 활성화
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        
        return output_path
