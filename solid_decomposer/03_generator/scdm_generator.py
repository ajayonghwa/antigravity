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
            # 플랜 타입별로 고유 인덱스 부여
            if plan["strategy"] == "OGRID":
                call = f"apply_ogrid('{plan['body_name']}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('max_radius', 1.0)}, {i})\n"
                execution_calls += call
            elif plan["strategy"] in ["AXIAL", "SECTOR", "HGRID"]:
                split = plan["split_plane"]
                call = f"apply_split_plane('{plan['body_name']}', {split['origin']}, {split['normal']}, '{plan['strategy']}', {i})\n"
                execution_calls += call

        script_template = f"""
# -*- coding: utf-8 -*-
import clr
import System
import math

ALL_CUTTERS = []

def get_matching_bodies(target_full_name):
    # 타겟 경로 추출
    parts = target_full_name.split("/")
    target_base = parts[-1]
    target_path = "/".join(parts[:-1]) if len(parts) > 1 else ""
    
    bodies = GetRootPart().GetAllBodies()
    targets = []
    for b in bodies:
        b_full = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_full = fn()
        except: pass
        
        b_parts = b_full.split("/")
        b_base = b_parts[-1]
        b_path = "/".join(b_parts[:-1]) if len(b_parts) > 1 else ""
        
        if b_path == target_path:
            if b_base == target_base or b_base.startswith(target_base + "_"):
                targets.append(b)
    return targets

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, max_r, idx):
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    frame = Frame.Create(origin_pt, direction)
    
    targets = get_matching_bodies(target_full_name)
    for i, target_body in enumerate(targets):
        try:
            # 커터 크기를 충분히 크게 (Unable to split 방지)
            cutter_size = max(max_r * 2.5, 0.005) 
            circle = Circle.Create(frame, cutter_size)
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            math_body = Body.CreatePlanarBody(plane, curve_array)
            
            # 완전 고유한 이름 부여
            tool_name = "Cutter_OGrid_" + str(idx) + "_" + str(i)
            tool_body = DesignBody.Create(GetRootPart(), tool_name, math_body)
            if tool_body: ALL_CUTTERS.append(tool_body)
            
            SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
        except Exception as e:
            print("O-grid error on " + target_full_name + ": " + str(e))

def apply_split_plane(target_full_name, origin_list, normal_list, strategy, idx):
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane_geom = Plane.Create(Frame.Create(origin, normal))
    
    try:
        tool_name = "Cutter_" + strategy + "_" + str(idx)
        tool_plane = DesignPlane.Create(GetRootPart(), tool_name, plane_geom)
        if tool_plane: ALL_CUTTERS.append(tool_plane)
    except: tool_plane = None

    targets = get_matching_bodies(target_full_name)
    if targets:
        try:
            cutter_sel = Selection.Create(tool_plane) if tool_plane else plane_geom
            SplitBody.ByCutter(Selection.Create(targets), cutter_sel, True)
        except: pass

def finalize():
    if ALL_CUTTERS:
        try:
            valid_cutters = [c for c in ALL_CUTTERS if not getattr(c, 'IsDeleted', False)]
            if valid_cutters:
                selection = Selection.Create(valid_cutters)
                # 컴포넌트로 이동
                new_occ = ComponentHelper.MoveBodiesToComponent(selection, None)
                if new_occ:
                    # Occurrence와 Template 모두 이름 변경 시도
                    try: 
                        new_occ.Name = "Decomposition_Tools"
                        new_occ.Template.Name = "Decomposition_Tools"
                    except: pass
                    print("Successfully grouped cutters into 'Decomposition_Tools'.")
        except Exception as e:
            print("Finalize error: " + str(e))

    try: GetRootPart().SharedTopology = PartSharedTopology.Share
    except: pass

# --- Start Execution ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
            
        # 가이드 문서 자동 생성 (생략 가능하면 패스)
        try:
            from scdm_bridge.guide_generator import GuideGenerator
            guide_md = GuideGenerator.generate_markdown(plan_list[0]['body_name'] if plan_list else "Body", "AXISYMMETRIC", plan_list)
            with open(os.path.join(self.output_dir, "Decomposition_Guide.md"), "w", encoding="utf-8") as f:
                f.write(guide_md)
        except: pass

        return output_path
