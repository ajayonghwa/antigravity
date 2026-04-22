import os
import clr
import System

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.output_dir = os.path.join(project_root, "04_script")
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir)
            except: self.output_dir = project_root

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

        script_template = f"""
# -*- coding: utf-8 -*-
# SCDM Script: Fixed Units (Meters) & Direct Component Parentage
import clr
import System
import math

def get_tool_component():
    root = GetRootPart()
    for comp in root.Components:
        if comp.Template.Name == "Decomposition_Tools":
            return comp
    try:
        doc = GetActiveDocument()
        return doc.CreateComponent("Decomposition_Tools")
    except:
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
        if "/".join(b_full.split("/")[:-1]) == target_path:
            b_name = b_full.split("/")[-1]
            if b_name == target_base or b_name.startswith(target_base):
                targets.append(b)
    return targets

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, ns_names):
    tool_comp = get_tool_component()
    # [중요] Meters 단위를 그대로 사용 (MM 제거)
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
    targets = get_matching_bodies(target_full_name)
    for target_body in targets:
        try:
            # 시각화용 원판 (Meters 단위 그대로 사용)
            circle = Circle.Create(frame, core_offset * 1.5)
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            math_body = Body.CreatePlanarBody(plane, curve_array)
            
            # [중요] 생성 시점에 부모 컴포넌트 즉시 지정
            tool_body = DesignBody.Create(tool_comp, "Cutter_OGrid", math_body)
            
            SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
            
            # 네임드 셀렉션
            if "core" in ns_names or "outer" in ns_names:
                res = GetRootPart().GetAllBodies() # 갱신된 바디들
                # (생략: 네임드 셀렉션 로직)
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    try:
        # 충분히 큰 칼날 (0.5m = 500mm)
        tool_plane = DesignPlane.Create(tool_comp, "Cutter_HGrid", plane_geom)
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
        DesignPlane.Create(tool_comp, "Cutter_Sector", plane_geom)
    except: pass
    
    targets = get_matching_bodies(target_full_name)
    if targets:
        try:
            SplitBody.ByCutter(Selection.Create(targets), plane_geom)
        except: pass

def finalize():
    print("Partitioning Finished.")

# --- Start Execution ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        return output_path
