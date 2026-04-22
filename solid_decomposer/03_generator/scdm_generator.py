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
            if plan["strategy"] == "OGRID":
                call = f"apply_ogrid('{plan['body_name']}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
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
        if b_parts[-1] == target_base or b_parts[-1].startswith(target_base + "_"):
            targets.append(b)
    return targets

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, idx):
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    
    targets = get_matching_bodies(target_full_name)
    for i, target_body in enumerate(targets):
        try:
            # 1. 원형 커브(Edge) 생성
            circle = Circle.Create(Frame.Create(origin_pt, direction), core_offset)
            curve_seg = CurveSegment.Create(circle)
            design_curve = DesignCurve.Create(GetRootPart(), curve_seg)
            
            # 2. ExtrudeEdges를 이용한 원통형 서피스 생성 (사용자 힌트 적용)
            # 타겟 바디를 충분히 관통하도록 길게 돌출
            extrude_dist = 0.5 
            # 시작점을 뒤로 밀어서 양방향 관통 효과 유도
            move_vec = Vector.Create(-direction.X * extrude_dist/2, -direction.Y * extrude_dist/2, -direction.Z * extrude_dist/2)
            Move.Execute(Selection.Create(design_curve), move_vec)
            
            options = ExtrudeEdgeOptions()
            options.PullType = PullType.Add
            # 엣지 선택 및 돌출 실행
            sel = Selection.Create(design_curve.Edge)
            result = ExtrudeEdges.Execute(sel, direction, extrude_dist, options)
            
            # 생성된 서피스 바디 찾기
            tool_body = None
            if result.CreatedBodies.Count > 0:
                tool_body = result.CreatedBodies[0]
                tool_body.Name = "Cutter_OGrid_" + str(idx) + "_" + str(i)
                ALL_CUTTERS.append(tool_body)
                
                # 3. 분할 실행
                try:
                    SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True)
                except: pass
            
            # 임시 커브 삭제
            design_curve.Delete()
        except Exception as e:
            print("O-grid error: " + str(e))

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
    for target in targets:
        try:
            cutter_sel = Selection.Create(tool_plane) if tool_plane else plane_geom
            SplitBody.ByCutter(Selection.Create(target), cutter_sel, True)
        except: pass

def finalize():
    if ALL_CUTTERS:
        try:
            valid_cutters = [c for c in ALL_CUTTERS if not getattr(c, 'IsDeleted', False)]
            if valid_cutters:
                new_occ = ComponentHelper.MoveBodiesToComponent(Selection.Create(valid_cutters), None)
                if new_occ:
                    try: 
                        new_occ.Name = "Decomposition_Tools"
                        new_occ.Template.Name = "Decomposition_Tools"
                    except: pass
        except: pass
    try: GetRootPart().SharedTopology = PartSharedTopology.Share
    except: pass

# --- Execution ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
            
        try:
            from scdm_bridge.guide_generator import GuideGenerator
            guide_md = GuideGenerator.generate_markdown(plan_list[0]['body_name'] if plan_list else "Body", "AXISYMMETRIC", plan_list)
            with open(os.path.join(self.output_dir, "Decomposition_Guide.md"), "w", encoding="utf-8") as f:
                f.write(guide_md)
        except: pass

        return output_path
