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
import clr
import System
import math

# 전역 도구 바구니 (나중에 한꺼번에 이동시키기 위함)
ALL_CUTTERS = []

def get_tool_component():
    root = GetRootPart()
    for comp in root.Components:
        if comp.Template.Name == "Decomposition_Tools":
            return comp
    # 사용자 힌트: ComponentHelper를 이용한 생성
    try: return ComponentHelper.Create(root, "Decomposition_Tools")
    except: return root

def move_to_tool_folder(tool_body):
    if tool_body:
        ALL_CUTTERS.append(tool_body)

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
    origin_pt = Point.Create(MM(center_list[0]), MM(center_list[1]), MM(center_list[2]))
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
    targets = get_matching_bodies(target_full_name)
    for target_body in targets:
        try:
            # 시각화를 위해 원판 도구 생성 (코어보다 크게 생성하여 식별 용이)
            circle = Circle.Create(frame, MM(core_offset * 1.5))
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            math_body = Body.CreatePlanarBody(plane, curve_array)
            tool_body = DesignBody.Create(GetRootPart(), "Cutter_OGrid", math_body)
            move_to_tool_folder(tool_body)
            
            res = SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
            # 네임드 셀렉션 부여
            if res and res.Success and res.CreatedBodies.Count >= 2:
                core_bodies = []
                outer_bodies = []
                for cb in res.CreatedBodies:
                    cg = cb.GetBoundingBox(Matrix.Identity).Center
                    dist = math.sqrt((cg.X - origin_pt.X)**2 + (cg.Y - origin_pt.Y)**2)
                    if dist < MM(core_offset): core_bodies.append(cb)
                    else: outer_bodies.append(cb)
                if core_bodies and "core" in ns_names: Selection.Create(core_bodies).CreateGroup(ns_names["core"])
                if outer_bodies and "outer" in ns_names: Selection.Create(outer_bodies).CreateGroup(ns_names["outer"])
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    origin = Point.Create(MM(origin_list[0]), MM(origin_list[1]), MM(origin_list[2]))
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    # 큼직한 평면 도구 생성 (500mm)
    try:
        tool_plane = DesignPlane.Create(GetRootPart(), "Cutter_HGrid", plane_geom)
        move_to_tool_folder(tool_plane)
    except: tool_plane = None

    targets = get_matching_bodies(target_full_name)
    for target in targets:
        try:
            if tool_plane: SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool_plane), True)
            else: SplitBody.ByCutter(Selection.Create(target), plane_geom)
        except: pass

def apply_sector(target_full_name, origin_list, normal_list, ns_names):
    origin = Point.Create(MM(origin_list[0]), MM(origin_list[1]), MM(origin_list[2]))
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    try:
        tool_plane = DesignPlane.Create(GetRootPart(), "Cutter_Sector", plane_geom)
        move_to_tool_folder(tool_plane)
    except: tool_plane = None
    
    targets = get_matching_bodies(target_full_name)
    if targets:
        try:
            if tool_plane: SplitBody.ByCutter(Selection.Create(targets), Selection.Create(tool_plane), True)
            else: SplitBody.ByCutter(Selection.Create(targets), plane_geom)
        except: pass

def finalize():
    # 마지막에 모든 커터를 모아서 이동 (사용자 힌트 적용)
    if ALL_CUTTERS:
        try:
            tool_comp = get_tool_component()
            selection = Selection.Create(ALL_CUTTERS)
            ComponentHelper.MoveBodiesToComponent(selection, tool_comp)
            print("All cutters moved to 'Decomposition_Tools' component.")
        except Exception as e:
            print("Failed to move cutters: " + str(e))
    
    try: GetRootPart().SharedTopology = PartSharedTopology.Share
    except: pass

# --- Start Execution ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        return output_path
