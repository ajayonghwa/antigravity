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
            elif strat in ["AXIAL", "SECTOR", "HGRID"]:
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

# [강화] 스페이스클레임 API 로드 (여러 버전 대응)
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
            
            # 2. 원통형 커터 생성을 위한 돌출(Extrude) 로직
            extrude_dist = 0.5 
            shifted_origin = Point.Create(origin_pt.X - direction.X * extrude_dist/2, 
                                          origin_pt.Y - direction.Y * extrude_dist/2, 
                                          origin_pt.Z - direction.Z * extrude_dist/2)
            
            circle = Circle.Create(Frame.Create(shifted_origin, direction), core_offset)
            design_curve = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle))
            
            tool_body = None
            try:
                # [무적 로직] 실행 전 바디 목록 기록
                bodies_before = list(GetRootPart().GetAllBodies())
                sel = Selection.Create(design_curve)
                
                try:
                    # 4개 인자 방식 시도
                    ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
                except:
                    # 5개 인자 방식 시도
                    ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
                
                # 실행 후 새로 생긴 바디 찾기
                bodies_after = list(GetRootPart().GetAllBodies())
                new_bodies = [b for b in bodies_after if b not in bodies_before]
                if new_bodies:
                    tool_body = new_bodies[0]
                
            except Exception as e:
                print("Extrude error: " + str(e))
                # [최종 보루] Pull 도구 시도
                try:
                    bodies_before = list(GetRootPart().GetAllBodies())
                    Pull.Execute(Selection.Create(design_curve), direction, extrude_dist, PullOptions(), None)
                    bodies_after = list(GetRootPart().GetAllBodies())
                    new_bodies = [b for b in bodies_after if b not in bodies_before]
                    if new_bodies: tool_body = new_bodies[0]
                except: pass
            
            if tool_body:
                tool_body.Name = "Cutter_OGrid_Cyl_" + str(idx) + "_" + str(i)
                ALL_CUTTERS.append(tool_body)
                try:
                    # [최종 확인된 형식] 4개 인자: Target, Cutter, Boolean, Info
                    SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True, None)
                except: pass
            
            design_curve.Delete()
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_split_plane(target_full_name, origin_list, normal_list, strategy, idx):
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    
    # [최종 전략] O-Grid와 동일하게 서피스 커터를 생성하여 분할
    try:
        # 1. 충분히 큰 사각형 커브 생성 (바디를 다 덮을 정도)
        size = 1.0 
        rect = Rectangle.Create(frame, size, size)
        design_curve = DesignCurve.Create(GetRootPart(), CurveSegment.Create(rect))
        
        # 2. 서피스로 돌출 (O-Grid 방식 재활용)
        extrude_dist = 0.001 # 아주 얇게 돌출시켜 서피스 생성
        bodies_before = list(GetRootPart().GetAllBodies())
        
        try:
            # 4개 인자 방식으로 돌출 시도
            ExtrudeEdges.Execute(Selection.Create(design_curve), extrude_dist, ExtrudeEdgeOptions(), None)
        except:
            # 5개 인자 방식으로 재시도
            ExtrudeEdges.Execute(Selection.Create(design_curve), Selection.Create(normal), extrude_dist, ExtrudeEdgeOptions(), None)
            
        bodies_after = list(GetRootPart().GetAllBodies())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        
        if new_bodies:
            tool_body = new_bodies[0]
            tool_body.Name = "Cutter_Surface_" + strategy + "_" + str(idx)
            ALL_CUTTERS.append(tool_body)
            
            # 3. 분할 실행 (검증된 4인자 방식)
            targets = get_matching_bodies(target_full_name)
            for target in targets:
                try:
                    SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool_body.Faces[0]), True, None)
                except: pass
        
        design_curve.Delete()
    except Exception as e:
        print(strategy + " split error: " + str(e))

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
