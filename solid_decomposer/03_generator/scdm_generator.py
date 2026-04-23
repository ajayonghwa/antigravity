# -*- coding: utf-8 -*-
import os
import json as pyjson
import base64

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.output_dir = os.path.join(project_root, "04_scripts")
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir)
            except: self.output_dir = project_root

    def generate_script(self, plan_list, output_name="scdm_decomposition_script.py", units="m"):
        execution_calls = ""
        comp_creation_calls = ""
        print("\n[Generating Script: {0}]".format(output_name))
        print(" - Total plans to process: {0}".format(len(plan_list)))
        
        # [v6.0] OneClickMaster 지원을 위한 컴포넌트 생성 및 실행 호출 구성
        body_indices = sorted(list(set(plan.get("body_index", 0) for plan in plan_list)))
        for b_idx in body_indices:
            comp_creation_calls += "_init_comp('', {0})\n".format(b_idx)

        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body_b64 = plan.get("body_b64")
            body_idx = plan.get("body_index", 0)
            
            if strat == "OGRID":
                center = plan['center']
                axis = plan['axis']
                offset = plan['core_offset']
                execution_calls += "apply_ogrid('{0}', {1}, {2}, {3}, {4}, {5})\n".format(
                    body_b64, pyjson.dumps(center), pyjson.dumps(axis), offset, i, body_idx)
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan.get("split_plane")
                if not split: continue
                origin = split['origin']
                normal = split.get('normal', [0,0,1])
                execution_calls += "apply_split_plane('{0}', {1}, {2}, '{3}', {4}, {5})\n".format(
                    body_b64, pyjson.dumps(origin), pyjson.dumps(normal), strat, i, body_idx)

        # [v6.0] stable_v1_backup의 정수를 담은 최종 템플릿
        script_template = """# -*- coding: utf-8 -*-
import clr
import System
# [v6.3] stable_v1_backup과 100% 동일한 임포트 구조로 원복
def initialize_api():
    for v in range(22, 16, -1):
        try:
            ref = "SpaceClaim.Api.V" + str(v)
            clr.AddReference(ref)
            exec("from SpaceClaim.Api.V" + str(v) + " import *", globals())
            exec("from SpaceClaim.Api.V" + str(v) + ".Modeler import *", globals())
            exec("from SpaceClaim.Api.V" + str(v) + ".Commands import *", globals())
            return True
        except: pass
    return False

initialize_api()

ALL_CUTTERS = []
BODY_COMP_MAP = {}

def get_matching_bodies(body_b64):
    try: t_clean = base64.b64decode(body_b64).decode('utf-8').lower().strip()
    except: t_clean = body_b64.lower().strip()
    try:
        # 백업본 방식: GetRootPart() 사용
        all_b = GetRootPart().GetAllBodies()
        target_base = t_clean.split("/")[-1]
        matches = [b for b in all_b if b.Name.lower().startswith(target_base)]
        return matches
    except: return []

def _init_comp(name_b64, body_idx):
    try:
        root = GetRootPart()
        comp_name = "CUTTERS_{0}".format(body_idx)
        target_comp = next((c for c in root.Components if c.Name == comp_name), None)
        if not target_comp:
            target_part = Part.Create(root.Document, comp_name)
            target_comp = Component.Create(root, target_part)
        BODY_COMP_MAP[body_idx] = target_comp
    except: pass

def _move_to_comp(obj, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try:
        # 백업본의 Selection.Create 사용
        sel = Selection.Create(obj)
        ComponentHelper.MoveBodiesToComponent(sel, target_comp)
    except: pass

def apply_ogrid(body_b64, center_list, axis_list, core_offset, idx, b_idx):
    origin_pt = Point.Create(center_list[0], center_list[1], center_list[2])
    direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
    
    targets = get_matching_bodies(body_b64)
    for target_body in targets:
        try:
            print("   [DEBUG] O-Grid Start for " + target_body.Name)
            extrude_dist = 0.5 
            shifted_origin = Point.Create(origin_pt.X - direction.X * extrude_dist/2, 
                                          origin_pt.Y - direction.Y * extrude_dist/2, 
                                          origin_pt.Z - direction.Z * extrude_dist/2)
            
            # [v6.3] 백업본 스타일 Frame 생성 (ref_x 결합)
            ref_x = Direction.DirX if abs(axis_list[0]) < 0.9 else Direction.DirY
            temp_frame = Frame.Create(shifted_origin, direction, ref_x)
            circle = Circle.Create(temp_frame, core_offset)
            
            # [v6.4] 4단계 무적 커브 생성 로직 (clr.Convert 활용)
            dc = None
            try:
                # Step 1: 정석적인 CurveSegment 방식
                dc = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle))
            except:
                try:
                    # Step 2: ITrimmedCurve로 강제 캐스팅 (IronPython 특화)
                    import clr
                    geom = clr.Convert(CurveSegment.Create(circle), ITrimmedCurve)
                    dc = DesignCurve.Create(GetRootPart(), geom)
                except:
                    try:
                        # Step 3: Circle 객체 직접 전달 시도
                        dc = DesignCurve.Create(GetRootPart(), circle)
                    except:
                        # Step 4: 최후의 보루
                        dc = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle).AsTrimmedCurve())
            
            if not dc: raise Exception("All DesignCurve creation methods failed")
            print("   [DEBUG] DesignCurve created successfully")
            
            tool_body = None
            try:
                bodies_before = list(GetRootPart().GetAllBodies())
                sel = Selection.Create(dc)
                
                try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
                except: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
                
                bodies_after = list(GetRootPart().GetAllBodies())
                new_bodies = [b for b in bodies_after if b not in bodies_before]
                if new_bodies: tool_body = new_bodies[0]
            except:
                try:
                    bodies_before = list(GetRootPart().GetAllBodies())
                    Pull.Execute(Selection.Create(dc), direction, extrude_dist, PullOptions(), None)
                    bodies_after = list(GetRootPart().GetAllBodies())
                    new_bodies = [b for b in bodies_after if b not in bodies_before]
                    if new_bodies: tool_body = new_bodies[0]
                except: pass
            
            if tool_body:
                ALL_CUTTERS.append(tool_body)
                try:
                    SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(tool_body.Faces[0]), True, None)
                except: pass
                _move_to_comp(tool_body, b_idx)
            
            dc.Delete()
            print("   [OK] O-Grid Success")
        except Exception as e:
            print("   [ERROR] O-grid fail: " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    
    ref_x = Direction.DirX if abs(normal_list[0]) < 0.9 else Direction.DirY
    frame = Frame.Create(origin, normal, ref_x)
    
    try:
        huge_radius = 5.0 
        circle_geom = Circle.Create(frame, huge_radius)
        # [v6.4] 평면 분할 시에도 4단계 무적 커브 생성 로직 적용
        dc = None
        try:
            dc = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle_geom))
        except:
            try:
                import clr
                geom = clr.Convert(CurveSegment.Create(circle_geom), ITrimmedCurve)
                dc = DesignCurve.Create(GetRootPart(), geom)
            except:
                try:
                    dc = DesignCurve.Create(GetRootPart(), circle_geom)
                except:
                    dc = DesignCurve.Create(GetRootPart(), CurveSegment.Create(circle_geom).AsTrimmedCurve())
        
        if not dc: raise Exception("All DesignCurve creation methods failed")
        
        bodies_before = list(GetRootPart().GetAllBodies())
        sel = Selection.Create(dc)
        try: Fill.Execute(sel, None)
        except: Fill.Execute(sel)
            
        bodies_after = list(GetRootPart().GetAllBodies())
        new_bodies = [b for b in bodies_after if b not in bodies_before]
        
        if new_bodies:
            tool_body = new_bodies[0]
            ALL_CUTTERS.append(tool_body)
            
            targets = get_matching_bodies(body_b64)
            for target in targets:
                try:
                    SplitBody.ByCutter(Selection.Create(target), Selection.Create(tool_body.Faces[0]), True, None)
                except: pass
            _move_to_comp(tool_body, b_idx)
        
        dc.Delete()
        print("   [OK] " + strategy + " split success")
    except Exception as e:
        print("   [ERROR] " + strategy + " split error: " + str(e))

def finalize():
    if ALL_CUTTERS:
        try:
            for cutter in ALL_CUTTERS:
                try: cutter.Delete()
                except: pass
            PartSharedTopology.Share(GetRootPart(), None)
        except: pass

# --- Execution ---
REPLACE_COMP_CREATION
REPLACE_EXECUTION
finalize()
print("Decomposition Finished.")
"""
        script_content = script_template.replace("REPLACE_COMP_CREATION", comp_creation_calls)
        script_content = script_content.replace("REPLACE_EXECUTION", execution_calls)
        
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f: f.write(script_content)
        return output_path
