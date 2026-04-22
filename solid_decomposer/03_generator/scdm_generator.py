import os

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.script_template = """
# -*- coding: utf-8 -*-
# Auto-generated SpaceClaim Script for Solid Decomposition
import clr
import System

def apply_ogrid(target_full_name, center_list, axis_list, core_offset, ns_names):
    # [지능형 개선] 컴포넌트 경로 인식 및 중복 이름 대응
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
            is_match = False
            if b_base == target_base:
                is_match = True
            elif b_base.startswith(target_base):
                suffix = b_base[len(target_base):]
                if not suffix or suffix[0].isdigit() or suffix[0] in [" ", "(", "-", "_"]:
                    is_match = True
            if is_match:
                targets.append(b)
    
    if not targets:
        print("Body not found: " + target_full_name)
        return

    for target_body in targets:
        tool_body = None
        try:
            print("O-grid Splitting for: " + target_full_name)
            circle = Circle.Create(frame, core_offset)
            curve_seg = CurveSegment.Create(circle)
            plane = Plane.Create(frame)
            
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            
            math_body = Body.CreatePlanarBody(plane, curve_array)
            tool_body = DesignBody.Create(GetRootPart(), "Ogrid_Tool", math_body)
            
            target_sel = Selection.Create(target_body)
            cutter_sel = Selection.Create(tool_body.Faces[0])
            
            try:
                res = SplitBody.ByCutter(target_sel, cutter_sel, True)
                if res and res.Success and res.CreatedBodies.Count >= 2:
                    core_bodies = []
                    outer_bodies = []
                    for cb in res.CreatedBodies:
                        cg = cb.GetBoundingBox(Matrix.Identity).Center
                        dist = ((cg.X - origin_pt.X)**2 + (cg.Y - origin_pt.Y)**2)**0.5
                        if dist < core_offset:
                            core_bodies.append(cb)
                        else:
                            outer_bodies.append(cb)
                    
                    if core_bodies and "core" in ns_names:
                        Selection.Create(core_bodies).CreateGroup(ns_names["core"])
                    if outer_bodies and "outer" in ns_names:
                        Selection.Create(outer_bodies).CreateGroup(ns_names["outer"])
            except: pass
        except Exception as e:
            print("O-grid error: " + str(e))
        finally:
            if tool_body: tool_body.Delete()

def apply_hgrid(target_full_name, origin_list, normal_list, ns_names):
    # [지능형 개선] 컴포넌트 경로 인식 및 중복 이름 대응
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
            is_match = False
            if b_base == target_base:
                is_match = True
            elif b_base.startswith(target_base):
                suffix = b_base[len(target_base):]
                if not suffix or suffix[0].isdigit() or suffix[0] in [" ", "(", "-", "_"]:
                    is_match = True
            if is_match:
                targets.append(b)
            
    if not targets:
        print("Body not found: " + target_full_name)
        return

    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane = Plane.Create(Frame.Create(origin, normal))
    
    print("Path-aware Sequential Splitting for: " + target_full_name)
    all_new_fragments = []
    for target in targets:
        try:
            res = SplitBody.ByCutter(Selection.Create(target), plane)
            if res and res.Success:
                all_new_fragments.extend([cb for cb in res.CreatedBodies])
            else:
                all_new_fragments.append(target)
        except:
            all_new_fragments.append(target)

    # 4. 네임드 셀렉션 부여 (생성된 모든 조각 대상)
    if all_new_fragments and ns_names:
        mid = len(all_new_fragments) // 2
        try:
            if "part_a" in ns_names: Selection.Create(all_new_fragments[:mid]).CreateGroup(ns_names["part_a"])
            if "part_b" in ns_names: Selection.Create(all_new_fragments[mid:]).CreateGroup(ns_names["part_b"])
        except: pass


def apply_sector(target_full_name, origin_list, normal_list, ns_names):
    # [지능형 개선] 컴포넌트 경로를 인식하여 중복 이름 충돌 방지
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane = Plane.Create(Frame.Create(origin, normal))
    
    # 타겟의 부모 경로와 베이스 이름 분리
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

        # 1. 부모 경로가 일치하고 2. 이름이 규칙에 맞는지 확인
        if b_path == target_path:
            is_match = False
            if b_base == target_base:
                is_match = True
            elif b_base.startswith(target_base):
                suffix = b_base[len(target_base):]
                if not suffix or suffix[0].isdigit() or suffix[0] in [" ", "(", "-", "_"]:
                    is_match = True
            
            if is_match:
                targets.append(b)
            
    if targets:
        try:
            print("Path-aware Batch Splitting " + str(len(targets)) + " targets...")
            SplitBody.ByCutter(Selection.Create(targets), plane)
        except: pass

def finalize():
    print("Applying Shared Topology for Conformal Meshing...")
    try:
        # 1. 파트 속성 방식 (일반적인 접근)
        GetRootPart().SharedTopology = PartSharedTopology.Share
    except:
        pass
        
    try:
        # 2. 스페이스클레임 도구 실행 방식 (2024 R1에서 직접 자른 후 강제 적용)
        options = ShareTopologyOptions()
        options.Tolerance = MM(0.2)
        # Info 자리에 None이나 빈 Selection을 주면 전체 대상
        ShareTopology.FindAndFix(options, None)
    except Exception as e:
        print("ShareTopology Fix failed (might not be necessary): " + str(e))
        
    print("All operations completed successfully.")

# --- Execution ---
{execution_calls}
finalize()
"""



    def generate_script(self, plan_list, output_name="final_scdm_script.py"):
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
        
        final_content = self.script_template.format(execution_calls=execution_calls)
        
        # 1. 스페이스클레임 스크립트 저장
        output_path = os.path.join(self.project_root, "04_scripts", output_name)
        if not os.path.exists(os.path.dirname(output_path)): os.makedirs(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        # 2. [추가] 휴먼 가이드(Markdown) 자동 생성 통합
        try:
            from scdm_bridge.guide_generator import GuideGenerator
            # 전체 전략 이름을 전달하도록 수정 (예: JUNCTION_CORE)
            # plan_list가 비어있지 않다면 첫 번째 플랜의 body_name을 기준으로 생성
            main_strategy = "INTELLIGENT_DECOMPOSITION"
            if plan_list:
                # 상위 수준에서 결정된 전략이 있다면 그걸 사용 (보통 main_run.py에서 전달)
                pass 

            guide_md = GuideGenerator.generate_markdown(
                plan_list[0]['body_name'] if plan_list else "Unknown", 
                "ADVANCED_PLAN", 
                plan_list
            )
            guide_path = os.path.join(self.project_root, "04_scripts", "Decomposition_Guide.md")
            with open(guide_path, "w", encoding="utf-8") as f:
                f.write(guide_md)
            print(f"Human Guide generated at: {guide_path}")
        except Exception as e:
            print(f"Guide generation skipped: {e}")
        
        return output_path

if __name__ == "__main__":
    # 테스트용 모의 계획
    mock_plan = [{
        "body_name": "Test_Cylinder",
        "strategy": "OGRID",
        "center": [0, 0, 0],
        "axis": [0, 0, 1],
        "core_offset": 3.0,
        "named_selections": {"core": "VALVE_OGRID_CORE", "outer": "VALVE_OGRID_OUTER"}
    }]
    
    gen = SCDMGenerator(os.getcwd())
    gen.generate_script(mock_plan)
    print("Script generated in scripts/final_scdm_script.py")
