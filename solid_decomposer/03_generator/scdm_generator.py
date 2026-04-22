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
    # 도구들을 모아둘 전용 컴포넌트 생성 또는 가져오기
    root = GetRootPart()
    tool_comp = None
    for comp in root.Components:
        if comp.Template.Name == "Decomposition_Tools":
            tool_comp = comp
            break
    if not tool_comp:
        tool_comp = ComponentHelper.Create(root, "Decomposition_Tools")
    return tool_comp

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, ns_names):
    # [디버깅 보강] 도구 컴포넌트 확보
    tool_comp = get_tool_component()
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
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
        b_base = b_full.split("/")[-1]
        
        if b_path == target_path:
            is_match = (b_base == target_base or b_base.startswith(target_base))
            if is_match: targets.append(b)
    
    if not targets: return

    for target_body in targets:
        try:
            circle = Circle.Create(frame, core_offset)
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            math_body = Body.CreatePlanarBody(plane, curve_array)
            # 도구 보존 (삭제하지 않음)
            tool_body = DesignBody.Create(tool_comp, "Cutter_OGrid_for_" + target_base, math_body)
            
            res = SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
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
            print("O-grid error for " + target_full_name + ": " + str(e))

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    target_path = "/".join(target_full_name.split("/")[:-1])
    target_base = target_full_name.split("/")[-1]
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    # 1. 시각적 평면 도구 생성
    tool_plane = None
    try:
        tool_plane = DesignPlane.Create(tool_comp, "Cutter_HGrid_Z" + str(round(origin.Z, 1)), plane_geom)
    except: pass

    bodies = GetRootPart().GetAllBodies()
    targets = [b for b in bodies if "/".join(b.Name.split("/")[:-1]) == target_path and b.Name.split("/")[-1].startswith(target_base)]
    if not targets: return

    for target in targets:
        try:
            # 2. [핵심] 생성된 실물 평면을 도구로 사용 (보존 옵션 True)
            if tool_plane:
                SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool_plane), True)
            else:
                SplitBody.ByCutter(Selection.Create(target), plane_geom)
        except: pass

def apply_sector(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    target_path = "/".join(target_full_name.split("/")[:-1])
    target_base = target_full_name.split("/")[-1]
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    # 1. 시각적 평면 도구 생성
    tool_plane = None
    try:
        tool_plane = DesignPlane.Create(tool_comp, "Cutter_Sector_N" + str(round(normal.X, 1)), plane_geom)
    except: pass
    
    bodies = GetRootPart().GetAllBodies()
    targets = [b for b in bodies if "/".join(b.Name.split("/")[:-1]) == target_path and b.Name.split("/")[-1].startswith(target_base)]
    
    if targets:
        try:
            # 2. [핵심] 생성된 실물 평면을 도구로 사용 (보존 옵션 True)
            if tool_plane:
                SplitBody.ByCutter(Selection.Create(targets), Selection.Create(tool_plane), True)
            else:
                SplitBody.ByCutter(Selection.Create(targets), plane_geom)
        except: pass

def finalize():
    print("Applying Shared Topology...")
    try:
        GetRootPart().SharedTopology = PartSharedTopology.Share
        options = ShareTopologyOptions()
        options.Tolerance = MM(0.2)
        ShareTopology.FindAndFix(options, None)
    except: pass
    print("All decomposition operations completed.")

# --- Planned Execution ---
{execution_calls}
finalize()
"""

    def generate_script(self, plan_list, output_filename="scdm_decomposition_script.py"):
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
        
        output_path = os.path.join(self.project_root, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_script)
            
        # 가이드 문서도 자동 생성 (scdm_bridge 모듈 이용)
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
