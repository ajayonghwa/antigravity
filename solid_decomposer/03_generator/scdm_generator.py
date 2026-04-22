import os
import clr
import System

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        # 04_scripts 폴더 경로 수정 (복수형)
        self.output_dir = os.path.join(project_root, "04_scripts")
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

ALL_CUTTERS = []

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
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
    targets = get_matching_bodies(target_full_name)
    for target_body in targets:
        try:
            circle = Circle.Create(frame, core_offset * 1.5)
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            math_body = Body.CreatePlanarBody(plane, curve_array)
            
            # 1. 루트 파트에 도구 생성
            tool_body = DesignBody.Create(GetRootPart(), "Cutter_OGrid", math_body)
            if tool_body: ALL_CUTTERS.append(tool_body)
            
            SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
            
            # 2. 네임드 셀렉션
            if "core" in ns_names or "outer" in ns_names:
                pass # (생략)
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    try:
        tool_plane = DesignPlane.Create(GetRootPart(), "Cutter_HGrid", plane_geom)
        if tool_plane: ALL_CUTTERS.append(tool_plane)
    except: pass

    targets = get_matching_bodies(target_full_name)
    for target in targets:
        try:
            SplitBody.ByCutter(Selection.Create(target), plane_geom)
        except: pass

def apply_sector(target_full_name, origin_list, normal_list, ns_names):
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    try:
        # 섹터 분할 평면에도 고유 이름 부여
        tool_name = "Cutter_Sector_Z" + str(round(origin.Z * 1000, 1))
        tool_plane = DesignPlane.Create(GetRootPart(), tool_name, plane_geom)
        if tool_plane: ALL_CUTTERS.append(tool_plane)
    except: tool_plane = None
    
    targets = get_matching_bodies(target_full_name)
    if targets:
        try:
            # 커터 평면이 성공적으로 생성되었다면 그것을 사용, 아니면 기하 평면 사용
            cutter_selection = Selection.Create(tool_plane) if tool_plane else plane_geom
            SplitBody.ByCutter(Selection.Create(targets), cutter_selection, True)
        except: pass

def finalize():
    # 사용자 힌트 적용: 모든 도구를 나중에 한꺼번에 컴포넌트로 이동
    if ALL_CUTTERS:
        try:
            valid_cutters = [c for c in ALL_CUTTERS if not getattr(c, 'IsDeleted', False)]
            if valid_cutters:
                selection = Selection.Create(valid_cutters)
                # None을 전달하여 새 컴포넌트를 만들고 그곳으로 이동시킵니다.
                new_comp = ComponentHelper.MoveBodiesToComponent(selection, None)
                if new_comp:
                    new_comp.Name = "Decomposition_Tools"
                    print("Successfully grouped cutters into 'Decomposition_Tools'.")
        except Exception as e:
            print("Failed to group cutters: " + str(e))

    try: GetRootPart().SharedTopology = PartSharedTopology.Share
    except: pass

# --- Start Execution ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
            
        # 가이드 문서 자동 생성 로직 복구
        try:
            from scdm_bridge.guide_generator import GuideGenerator
            guide_md = GuideGenerator.generate_markdown(
                plan_list[0]['body_name'] if plan_list else "Unknown", 
                "ADVANCED_PLAN", 
                plan_list
            )
            guide_path = os.path.join(self.output_dir, "Decomposition_Guide.md")
            with open(guide_path, "w", encoding="utf-8") as f:
                f.write(guide_md)
            print(f" - Markdown guide generated: {guide_path}")
        except Exception as e:
            print(f" [Error] Guide generation failed: {str(e)}")
            import traceback
            traceback.print_exc()

        return output_path
