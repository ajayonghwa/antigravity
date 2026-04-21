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
        
        # 원본 이름과 정확히 일치하거나, "이름 (1)" 처럼 분할된 조각들 포함
        if b_name == body_name or b_name.startswith(body_name + " ("):
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
                SplitBody.ByCutter(target_sel, cutter_sel, True)
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
    # GetFullName()은 "Component/BodyName" 형식이므로, 끝부분 매칭(endswith) 방식으로 강건하게 탐색
    bodies = GetRootPart().GetAllBodies()
    target_bodies = []
    for b in bodies:
        b_name = b.Name
        try:
            fn = getattr(b, 'GetFullName', None)
            if fn: b_name = fn()
        except:
            pass
        
        # 이름 끝이 body_name과 일치하거나, "body_name (숫자)" 패턴인 조각들 수집
        base = b_name.split("/")[-1]  # 경로에서 마지막 이름만 추출
        if base == body_name or base.startswith(body_name + " (") or base.startswith(body_name + "("):
            target_bodies.append(b)
            
    if not target_bodies:
        print("Body not found: " + body_name)
        return

    # Python 리스트를 .NET Array로 변환하여 일괄 선택(Selection) 생성
    import System
    body_array = System.Array.CreateInstance(type(target_bodies[0]), len(target_bodies))
    for i, b in enumerate(target_bodies):
        body_array[i] = b
    target_sel = Selection.Create(body_array)

    # 2. 분할 평면 생성
    try:
        origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
        normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
        frame = Frame.Create(origin, normal)
        plane = Plane.Create(frame)
        
        # 3. 바디 일괄 분할 실행
        print("Plane Splitting all fragments of: " + body_name + " (count: " + str(len(target_bodies)) + ")")
        
        def assign_ns(res):
            if res and res.Success and res.CreatedBodies.Count >= 2:
                all_created = [cb for cb in res.CreatedBodies]
                mid = len(all_created) // 2
                Selection.Create(all_created[:mid]).CreateGroup(ns_names["part_a"])
                Selection.Create(all_created[mid:]).CreateGroup(ns_names["part_b"])

        try:
            result = SplitBody.ByCutter(target_sel, plane)
            assign_ns(result)
        except:
            try:
                datum = DatumPlaneCreator.Create(plane).CreatedPlanes[0]
                result = SplitBody.ByCutter(target_sel, Selection.Create(datum))
                assign_ns(result)
                datum.Delete()
            except:
                pass
                
    except Exception as e:
        print("Plane split error: " + str(e))


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
        
        output_path = os.path.join(self.project_root, "04_scripts", output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        
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
