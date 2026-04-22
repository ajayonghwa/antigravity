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
# SCDM Decomposition Script (Optimized for User Environment)
import clr
import System
import math

def get_tool_component():
    root = GetRootPart()
    # 1. 기존 도구 컴포넌트 찾기
    for comp in root.Components:
        if comp.Template.Name == "Decomposition_Tools":
            return comp
    
    # 2. 새 컴포넌트 생성 (멀티 메소드 시도)
    try:
        # 방법 A: 표준 ComponentHelper
        return ComponentHelper.Create(root, "Decomposition_Tools")
    except:
        try:
            # 방법 B: Document 직접 생성
            doc = GetActiveDocument()
            if hasattr(doc, 'CreateComponent'):
                return doc.CreateComponent("Decomposition_Tools")
            return root
        except:
            return root

def get_matching_bodies(target_full_name):
    # 경로 기반 바디 추출 로직
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
            is_match = (b_name == target_base or b_name.startswith(target_base))
            if is_match: targets.append(b)
    return targets

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, ns_names):
    tool_comp = get_tool_component()
    origin_pt = Point.Create(MM(center_list[0]), MM(center_list[1]), MM(center_list[2]))
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
    targets = get_matching_bodies(target_full_name)
    if not targets: return

    for target_body in targets:
        try:
            # 사용자 힌트 반영: Plane.Create(Frame.Create(...)) 스타일
            section_plane = Plane.Create(frame)
            circle = Circle.Create(frame, MM(core_offset))
            curve_seg = CurveSegment.Create(circle)
            
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            
            math_body = Body.CreatePlanarBody(section_plane, curve_array)
            # 물리적 커터 보존
            tool_body = DesignBody.Create(tool_comp, "Cutter_OGrid", math_body)
            
            SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    origin = Point.Create(MM(origin_list[0]), MM(origin_list[1]), MM(origin_list[2]))
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    section_plane = Plane.Create(Frame.Create(origin, normal))
    
    # DatumPlane 스타일의 가시적 도구 생성
    try:
        DesignPlane.Create(tool_comp, "Cutter_HGrid", section_plane)
    except: pass

    targets = get_matching_bodies(target_full_name)
    for target in targets:
        try:
            SplitBody.ByCutter(Selection.Create(target), section_plane)
        except: pass

def apply_sector(target_full_name, origin_list, normal_list, ns_names):
    tool_comp = get_tool_component()
    origin = Point.Create(MM(origin_list[0]), MM(origin_list[1]), MM(origin_list[2]))
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    section_plane = Plane.Create(Frame.Create(origin, normal))
    
    try:
        DesignPlane.Create(tool_comp, "Cutter_Sector", section_plane)
    except: pass
    
    targets = get_matching_bodies(target_full_name)
    if targets:
        try:
            SplitBody.ByCutter(Selection.Create(targets), section_plane)
        except: pass

def finalize():
    try: GetRootPart().SharedTopology = PartSharedTopology.Share
    except: pass

# --- Start Execution ---
{execution_calls}
finalize()
"""

        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
            
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
        except: pass

        return output_path
