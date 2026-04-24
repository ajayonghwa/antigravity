import cadquery as cq
import json
import os
import sys
import shutil

# 경로 설정
sys.path.append(os.getcwd())
from src.extractor import GeometryExtractor
from src.executor import SplitExecutor
from demo_full_pipeline import export_svg_views, generate_report_html, generate_report_md

def create_complex_model_1():
    """Model 1: Flanged Pipe with Ribs (튜브 + 플랜지 + 보강재)"""
    tube = cq.Workplane("XY").circle(20).extrude(60).faces(">Z").workplane().hole(30)
    flange = cq.Workplane("XY").circle(40).extrude(10)
    # 보강재(Rib) 추가
    rib = cq.Workplane("XZ").rect(10, 40).extrude(5).translate((25, 0, 10))
    return tube.union(flange).union(rib)

def create_complex_model_2():
    """Model 2: L-Bracket with Boss (L자 브래킷 + 보스 + 구멍)"""
    base = cq.Workplane("XY").box(60, 20, 10).translate((30, 0, 5))
    upright = cq.Workplane("XY").box(10, 20, 50).translate((5, 0, 25))
    boss = cq.Workplane("YZ").workplane(offset=10).circle(10).extrude(20).translate((0,0,30))
    result = base.union(upright).union(boss)
    # 구멍 뚫기: 이제 result에 본체가 있으므로 연산 가능
    result = result.faces("<X").workplane(offset=10).circle(5).cutThruAll()
    return result

def create_complex_model_3():
    """Model 3: Stepped Plate with Pattern (단차판 + 구멍 패턴)"""
    plate = cq.Workplane("XY").box(100, 100, 10).translate((0,0,5))
    step = cq.Workplane("XY").box(50, 100, 10).translate((25, 0, 15))
    result = plate.union(step)
    # 구멍 패턴
    locs = [(25, 25), (25, -25), (-25, 25), (-25, -25)]
    for x, y in locs:
        result = result.faces(">Z").workplane().center(x, y).hole(10)
    return result

def run_pipeline_for_model(model_func, model_name, ai_plan):
    print(f"\n--- Processing {model_name} ---")
    model = model_func()
    output_dir = f"report_{model_name}"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # 1. 분석
    extractor = GeometryExtractor(model)
    summary = extractor.extract_summary()
    
    # 분석 결과(인풋)를 JSON으로 저장
    with open(os.path.join(output_dir, "geometry_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # AI 계획(아웃풋)을 JSON으로 저장
    with open(os.path.join(output_dir, "ai_plan.json"), "w", encoding="utf-8") as f:
        json.dump(ai_plan, f, indent=2, ensure_ascii=False)
    
    # 2. 시각화 (Before)
    before_views = export_svg_views(model, "before", output_dir)
    
    # 3. 분할 실행
    executor = SplitExecutor(model)
    solids = executor.execute_plan(ai_plan)
    
    # 4. 시각화 (After)
    combined_after = cq.Workplane("XY")
    for b in solids:
        combined_after = combined_after.add(b)
    after_views = export_svg_views(combined_after, "after", output_dir)
    
    # 5. 리포트 생성
    generate_report_html(output_dir, ai_plan, summary, before_views, after_views)
    generate_report_md(output_dir, ai_plan, summary)
    print(f"✅ {model_name} Complete!")

if __name__ == "__main__":
    # 각 모델별 AI 전략 정의
    plans = {
        "Model_1": {
            "strategy_description": "Rib & Flange Isolation",
            "reasoning": "보강 리브(Rib)와 플랜지 접합부는 메쉬가 꼬이기 쉬운 오목한 경계를 형성합니다. 리브 접합면을 따라 평면 절단을 수행하고 플랜지를 분리하여 독립된 스윕 영역을 확보합니다.",
            "splits": [
                {"operation": "plane_cut", "axis": "Z", "coordinate": 10.0, "reason": "Flange separation"},
                {"operation": "plane_cut", "axis": "X", "coordinate": 25.0, "reason": "Rib separation"}
            ]
        },
        "Model_2": {
            "strategy_description": "L-Bend & Boss Decomposition",
            "reasoning": "L자 굴곡부와 돌출된 보스(Boss)는 각각 다른 메쉬 흐름을 가집니다. 굴곡부 평면 절단과 보스 기부 절단을 통해 구조를 단순화합니다.",
            "splits": [
                {"operation": "plane_cut", "axis": "X", "coordinate": 10.0, "reason": "L-bend vertical cut"},
                {"operation": "plane_cut", "axis": "Z", "coordinate": 30.0, "reason": "Boss center cut"}
            ]
        },
        "Model_3": {
            "strategy_description": "Stepped Plate & Hole Pattern Isolation",
            "reasoning": "단차(Step)와 구멍 패턴이 섞여 있으므로, 우선 단차 평면을 따라 자르고 각 구멍 영역을 블록화하여 정렬된 메쉬를 생성할 수 있게 합니다.",
            "splits": [
                {"operation": "plane_cut", "axis": "X", "coordinate": 0.0, "reason": "Main step separation"},
                {"operation": "plane_cut", "axis": "Y", "coordinate": 0.0, "reason": "Symmetric pattern split"}
            ]
        }
    }

    run_pipeline_for_model(create_complex_model_1, "Model_1", plans["Model_1"])
    run_pipeline_for_model(create_complex_model_2, "Model_2", plans["Model_2"])
    run_pipeline_for_model(create_complex_model_3, "Model_3", plans["Model_3"])
    
    print("\n🚀 All 3 complex models processed successfully!")
