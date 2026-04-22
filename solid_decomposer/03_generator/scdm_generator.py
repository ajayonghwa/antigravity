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
    
    all_bodies = GetRootPart().GetAllBodies()
    matched = []
    for body in all_bodies:
        b_name = body.Name
        # 정확히 일치하거나, 분할되어 숫자가 붙은 경우(Body_1, Body_CORE 등) 모두 찾음
        if b_name == target_base or b_name.startswith(target_base + "_") or b_name.startswith(target_base + " ("):
            matched.append(body)
    return matched

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, idx):
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    
    targets = get_matching_bodies(target_full_name)
    for i, target_body in enumerate(targets):
        try:
            # 1. 원통형 커터 생성을 위한 돌출(Extrude) 로직
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
                    # [최종 확인된 형식] 4개 인자 호출
                    SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True, None)
                except: pass
            
            design_curve.Delete()
        except Exception as e:
            print("O-grid error: " + str(e))

def apply_split_plane(target_full_name, origin_list, normal_list, strategy, idx):
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    
    # [최종 전략] 원을 그린 뒤 내부를 채워(Fill) 평면 서피스 커터 생성
    try:
        # 1. 적당히 큰 원(반지름 1m) 생성
        huge_radius = 1.0 
        circle_geom = Circle.Create(frame, huge_radius)
        design_curve = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle_geom))
        
        # 2. Fill 명령어로 원 내부를 채워 서피스 바디 생성
        bodies_before = list(GetRootPart().GetAllBodies())
        try:
            Fill.Execute(Selection.Create(design_curve), None)
        except:
            Fill.Execute(Selection.Create(design_curve))
            
        bodies_after = list(GetRootPart().GetAllBodies())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        
        if new_bodies:
            tool_body = new_bodies[0]
            tool_body.Name = "Cutter_Surface_" + strategy + "_" + str(idx)
            ALL_CUTTERS.append(tool_body)
            
            # 3. 분할 실행 (4인자 방식)
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
            # 커터들 정리 및 공유 토폴로지 적용
            for cutter in ALL_CUTTERS:
                try: cutter.Delete()
                except: pass
            # 최종 바디들 간의 연결성 확보
            PartSharedTopology.Share(GetRootPart(), None)
        except: pass

# --- Execution ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        
        return output_path
