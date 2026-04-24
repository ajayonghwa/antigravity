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
    parser.add_argument("--max-parts", type=int, default=15, help="Maximum number of split parts allowed")
    parser.add_argument("--max-splits", type=int, default=None, help="Maximum number of splitting operations allowed")
    parser.add_argument("--min-volume", type=float, default=0.01, help="Minimum volume ratio (0.01 = 1%)")
    args = parser.parse_args()
    
    # max_splits가 지정되지 않은 경우 max_parts로부터 유추 (예: 16 parts -> 6 splits)
    if args.max_splits is None:
        import math
        # (n+1)^2 <= max_parts -> n+1 <= sqrt(max_parts) -> n <= sqrt(max_parts) - 1
        # splits = 2 * n
        n = int(math.sqrt(args.max_parts)) - 1
        args.max_splits = max(2, n * 2)

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
    planner = AIPlanner(max_splits=args.max_splits)
    ai_plan = planner.plan_splits(summary)
    
    # 리포트 생성을 위해 필수 키가 있는지 확인하고 기본값을 채웁니다.
    if not ai_plan: ai_plan = {}
    if "strategy_description" not in ai_plan:
        ai_plan["strategy_description"] = "Standard Decomposition"
    if "reasoning" not in ai_plan:
        ai_plan["reasoning"] = "AI provided no reasoning. Applying fallback heuristics."
    if "splits" not in ai_plan:
        ai_plan["splits"] = []

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
    solids = executor.execute_plan(ai_plan, max_parts=args.max_parts, min_volume_ratio=args.min_volume)
    
    # 7. 시각화 (After)
    combined_after = cq.Workplane("XY")
    for b in solids:
        combined_after = combined_after.add(b)
    after_views = export_svg_views(combined_after, "after", args.output)
    
    # [NEW] 분할된 개별 솔리드들을 STEP 파일로 저장
    parts_dir = os.path.join(args.output, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    for i, solid in enumerate(solids):
        part_path = os.path.join(parts_dir, f"part_{i:02d}.step")
        cq.exporters.export(cq.Workplane(solid), part_path)
    
    # 8. 최종 리포트 생성
    generate_report_html(args.output, ai_plan, summary, before_views, after_views)
    generate_report_md(args.output, ai_plan, summary)
    
    print(f"\n✅ All steps completed!")
    print(f"📦 Split Parts saved in: {parts_dir}")
    print(f"📊 Report: {args.output}/index.html")
    print(f"📝 Plan Detail: {args.output}/decomposition_report.md")

if __name__ == "__main__":
    main()
