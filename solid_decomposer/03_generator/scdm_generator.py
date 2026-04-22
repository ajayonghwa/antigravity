import os
import clr
import System

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.script_template = """
# -*- coding: utf-8 -*-
# Auto-generated SpaceClaim Script for Solid Decomposition
import clr
import System
import math

def get_tool_component():
    root = GetRootPart()
    for comp in root.Components:
        if comp.Template.Name == "Decomposition_Tools":
            return comp
    return ComponentHelper.Create(root, "Decomposition_Tools")

def get_matching_bodies(target_full_name):
    target_path = "/".join(target_full_name.split("/")[:-1])
    target_base = target_full_name.split("/")[-1]
    
    bodies = GetRootPart().GetAllBodies()
    targets = []
    for b in bodies:
        b_full = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_full = fn()
        except: pass
        
        b_path = "/".join(b_full.split("/")[:-1])
        b_name = b_full.split("/")[-1]
        
        if b_path == target_path:
            is_match = False
            if b_name == target_base: is_match = True
            elif b_name.startswith(target_base):
                suffix = b_name[len(target_base):]
                if not suffix or suffix[0].isdigit() or suffix[0] in [" ", "(", "-", "_"]:
                    is_match = True
            if is_match: targets.append(b)
    return targets

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, ns_names):
    tool_comp = get_tool_component()
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
    targets = get_matching_bodies(target_full_name)
    if not targets: return

    for target_body in targets:
        try:
            circle = Circle.Create(frame, core_offset)
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            math_body = Body.CreatePlanarBody(plane, curve_array)
            # 물리적 서피스 바디로 생성
            tool_body = DesignBody.Create(tool_comp, "OGrid_Cutter", math_body)
            
            res = SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
            # 네임드 셀렉션 부여
            if res and res.Success and res.CreatedBodies.Count >= 2:
                core_bodies = []
                outer_bodies = []
                for cb in res.CreatedBodies:
                    cg = cb.GetBoundingBox(Matrix.Identity).Center
                    dist = math.sqrt((cg.X - origin_pt.X)**2 + (cg.Y - origin_pt.Y)**2)
                    if dist < core_offset: core_bodies.append(cb)
                    else: outer_bodies.append(cb)
                if core_bodies and "core" in ns_names: Selection.Create(core_bodies).CreateGroup(ns_names["core"])
                if outer_bodies and "outer" in ns_names: Selection.Create(outer_bodies).CreateGroup(ns_names["outer"])
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    # [핵심] 시각화를 위해 충분히 큰 사각형 서피스 생성
    try:
        # 100mm 크기의 사각형 칼날 생성
        rect = Rectangle.Create(Frame.Create(origin, normal), 0.1, 0.1)
        # Rectangle의 Item1, Item2 등은 선분들임
        # 여기서는 단순하게 평면 객체로 자르되, 가시성을 위해 DesignPlane도 병행 생성
        DesignPlane.Create(tool_comp, "HGrid_Cutter_Z" + str(round(origin.Z, 1)), plane_geom)
    except: pass

    targets = get_matching_bodies(target_full_name)
    for target in targets:
        try:
            SplitBody.ByCutter(Selection.Create(target), plane_geom)
        except: pass

def apply_sector(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    try:
        DesignPlane.Create(tool_comp, "Sector_Cutter_N" + str(round(normal.X, 1)), plane_geom)
    except: pass
    
    targets = get_matching_bodies(target_full_name)
    if targets:
        try:
            SplitBody.ByCutter(Selection.Create(targets), plane_geom)
        except: pass

def finalize():
    print("Finalizing...")
    try:
        GetRootPart().SharedTopology = PartSharedTopology.Share
    except: pass

# --- Execution ---
{execution_calls}
finalize()
"""

    def generate_script(self, plan_list, output_name="scdm_decomposition_script.py"):
        execution_calls = ""
        for plan in plan_list:
            if plan["strategy"] == "OGRID":
                call = f"apply_ogrid('{plan['body_name']}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan['named_selections']})\n"
                execution_calls += call
            elif plan["strategy"] == "SECTOR":
                split = plan["split_plane"]
                call = f"apply_sector('{plan['body_name']}', {split['origin']}, {split['normal']}, {plan['named_selections']})\n"
                execution_calls += call
            elif plan["strategy"] in ["HGRID", "AXIAL", "JUNCTION", "TRANSVERSE"]:
                split = plan["split_plane"]
                call = f"apply_hgrid('{plan['body_name']}', {split['origin']}, {split['normal']}, {plan['named_selections']})\n"
                execution_calls += call

        full_script = self.script_template.format(execution_calls=execution_calls)
        output_path = os.path.join(self.project_root, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_script)
            
        try:
            from scdm_bridge.guide_generator import GuideGenerator
            guide_md = GuideGenerator.generate_markdown(
                plan_list[0]['body_name'] if plan_list else "Unknown", 
                "ADVANCED_PLAN", 
                plan_list
            )
            guide_path = os.path.join(self.project_root, "Decomposition_Guide.md")
            with open(guide_path, "w", encoding="utf-8") as f:
                f.write(guide_md)
        except Exception as e:
            print(f"Guide generation skipped: {e}")

        return output_path
