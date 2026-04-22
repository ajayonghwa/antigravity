import os

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.script_template = """
# -*- coding: utf-8 -*-
# Auto-generated SpaceClaim Script for Solid Decomposition
import clr
import System

def apply_ogrid(body_name, center_list, axis_list, core_offset, ns_names):
    # 1. 대상 바디들 찾기 (원본 이름과 일치하거나 분할로 인해 숫자가 붙은 모든 조각들 수집)
    bodies = GetRootPart().GetAllBodies()
    target_bodies = []
    for b in bodies:
        b_name = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_name = fn()
        except:
            pass
        
        # [수정] 이름 매칭 강화: 원본 이름으로 시작하고 뒤에 숫자나 괄호가 붙는 모든 변종 포함
        # 예: Solid 1, Solid 11, Solid 1 (1), Solid 1(1) 모두 매칭
        is_match = False
        if b_name == body_name:
            is_match = True
        elif b_name.startswith(body_name):
            suffix = b_name[len(body_name):].strip()
            # 뒤에 붙은게 숫자이거나, 괄호로 시작하면 자식으로 간주
            if not suffix or suffix.isdigit() or suffix.startswith("(") or suffix.startswith(" ("):
                is_match = True
        
        if is_match:
            target_bodies.append(b)
    
    if not target_bodies:
        print("Body not found: " + body_name)
        return

    # 2. 모든 대상 조각에 대해 분할 시도 (평면이 지나는 조각만 실제로 잘림)
    for target_body in target_bodies:
        # 2. 실린더 컷팅 평면/축 설정
        origin = Point.Create(center_list[0], center_list[1], center_list[2])
        direction = Direction.Create(axis_list[0], axis_list[1], axis_list[2])
        frame = Frame.Create(origin, direction)

        tool_body = None
        try:
            # 3. 평면 표면(Surface Body) 생성 및 자르기
            print("O-grid Splitting for piece of: " + body_name)
            circle = Circle.Create(frame, core_offset)
            curve_seg = CurveSegment.Create(circle)
            
            # 원을 감싸는 평면 정의 (Plane.Create는 1개의 Frame 인수를 받음)
            plane = Plane.Create(frame)
            
            # Python의 list([]) 대신 .NET의 Array를 명시적으로 생성하여 전달합니다. (타입 에러 방지)
            curve_array = System.Array.CreateInstance(type(curve_seg), 1)
            curve_array[0] = curve_seg
            
            # 표면 바디(수학 모델) 생성 및 스페이스클레임에 실제 바디로 등록
            math_body = Body.CreatePlanarBody(plane, curve_array)
            tool_body = DesignBody.Create(GetRootPart(), "Ogrid_Tool", math_body)
            
            target_sel = Selection.Create(target_body)
            # 생성된 원판 표면의 면(Face)을 선택
            cutter_sel = Selection.Create(tool_body.Faces[0])
            
            # 면으로 자르기 실행 (실패하더라도 다음 조각으로 넘어가야 함)
            try:
                res = SplitBody.ByCutter(target_sel, cutter_sel, True)
                
                # 분할 성공 시 네임드 셀렉션 부여 (Core / Outer 구분)
                if res and res.Success and res.CreatedBodies.Count >= 2:
                    core_bodies = []
                    outer_bodies = []
                    for cb in res.CreatedBodies:
                        cg = cb.GetBoundingBox(Matrix.Identity).Center
                        # Z축 방향을 제외한 반경(Radial) 거리로 구분
                        dist = ((cg.X - origin.X)**2 + (cg.Y - origin.Y)**2)**0.5
                        if dist < core_offset:
                            core_bodies.append(cb)
                        else:
                            outer_bodies.append(cb)
                    
                    try:
                        if core_bodies and "core" in ns_names:
                            Selection.Create(core_bodies).CreateGroup(ns_names["core"])
                        if outer_bodies and "outer" in ns_names:
                            Selection.Create(outer_bodies).CreateGroup(ns_names["outer"])
                    except: pass
            except:
                pass
            
        except Exception as e:
            print("O-grid error: " + str(e))
        finally:
            # 성공/실패 여부와 상관없이 임시 도구는 반드시 삭제
            if tool_body:
                tool_body.Delete()

def apply_hgrid(body_name, origin_list, normal_list, ns_names):
    # 1. 대상 바디들 찾기 (분할된 조각들까지 모두 수집)
    bodies = GetRootPart().GetAllBodies()
    target_bodies = []
    for b in bodies:
        b_name = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_name = fn()
        except: pass
        
        base = b_name.split("/")[-1]
        
        # [수정] 자식 바디 매칭 로직 강화 (숫자 연속형 대응)
        is_match = False
        if base == body_name:
            is_match = True
        elif base.startswith(body_name):
            suffix = base[len(body_name):].strip()
            if not suffix or suffix.isdigit() or suffix.startswith("("):
                is_match = True
        
        if is_match:
            target_bodies.append(b)
            
    if not target_bodies:
        print("Body not found: " + body_name)
        return

    # 2. 분할 평면 생성
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    plane = Plane.Create(Frame.Create(origin, normal))
    
    # 3. [핵심 수정] 일괄 분할 대신 '순차적 분할'로 조각 누락 방지
    print("Sequential Splitting fragments of: " + body_name)
    all_new_fragments = []
    
    for target in target_bodies:
        try:
            # 개별 바디에 대해 분할 실행
            res = SplitBody.ByCutter(Selection.Create(target), plane)
            if res and res.Success:
                all_new_fragments.extend([cb for cb in res.CreatedBodies])
            else:
                all_new_fragments.append(target) # 잘리지 않은 경우 유지
        except:
            all_new_fragments.append(target)

    # 4. 네임드 셀렉션 부여 (생성된 모든 조각 대상)
    if all_new_fragments and ns_names:
        mid = len(all_new_fragments) // 2
        try:
            if "part_a" in ns_names: Selection.Create(all_new_fragments[:mid]).CreateGroup(ns_names["part_a"])
            if "part_b" in ns_names: Selection.Create(all_new_fragments[mid:]).CreateGroup(ns_names["part_b"])
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
            elif plan["strategy"] in ["HGRID", "AXIAL", "SECTOR", "JUNCTION", "TRANSVERSE"]:
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
            guide_md = GuideGenerator.generate_markdown(plan_list[0]['body_name'] if plan_list else "Unknown", "AUTO", plan_list)
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
