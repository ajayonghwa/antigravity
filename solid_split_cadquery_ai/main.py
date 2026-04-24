import cadquery as cq
import json
import os
import sys
import shutil
import argparse

# 프로젝트 내부 모듈 임포트
sys.path.append(os.getcwd())
from src.extractor import GeometryExtractor
from src.executor import SplitExecutor
from demo_full_pipeline import export_svg_views, generate_report_html, generate_report_md

def main():
    parser = argparse.ArgumentParser(description="AI-Driven Solid Decomposition Tool")
    parser.add_argument("input", help="Path to the input STEP file")
    parser.add_argument("--output", default="output_report", help="Directory to save the report")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Error: File not found - {args.input}")
        return

    print(f"🚀 Processing: {args.input}")
    
    # 1. 모델 로드 (이미 존재하는 형상을 읽어옴)
    try:
        model = cq.importers.importStep(args.input)
    except Exception as e:
        print(f"❌ Error loading STEP file: {e}")
        return

    # 2. 형상 분석 (Extractor)
    print("🔍 Analyzing geometry features...")
    extractor = GeometryExtractor(model)
    summary = extractor.extract_summary()
    
    # 3. AI 전략 수립 (Planner)
    # 실시간으로 Ollama 로컬 AI에게 전략을 요청합니다.
    print("🧠 Planning decomposition strategy with AI (Ollama)...")
    from src.planner import AIPlanner
    planner = AIPlanner()
    ai_plan = planner.plan_splits(summary)
    
    if not ai_plan.get("splits"):
        print("⚠️ AI produced an empty plan. Using defaults.")

    # 4. 결과 디렉토리 정리
    if os.path.exists(args.output):
        shutil.rmtree(args.output)
    os.makedirs(args.output)

    # 5. 시각화 (Before)
    before_views = export_svg_views(model, "before", args.output)
    
    # 6. 분할 실행 (Executor)
    print("✂️ Executing splits...")
    executor = SplitExecutor(model)
    solids = executor.execute_plan(ai_plan)
    
    # 7. 시각화 (After)
    combined_after = cq.Workplane("XY")
    for b in solids:
        combined_after = combined_after.add(b)
    after_views = export_svg_views(combined_after, "after", args.output)
    
    # 8. 최종 리포트 생성
    generate_report_html(args.output, ai_plan, summary, before_views, after_views)
    generate_report_md(args.output, ai_plan, summary)
    
    print(f"\n✅ All steps completed!")
    print(f"📊 Report: {args.output}/index.html")
    print(f"📝 Plan Detail: {args.output}/decomposition_report.md")

if __name__ == "__main__":
    main()
