import cadquery as cq
import json
import os
import sys
import shutil
import glob
import argparse

# 프로젝트 내부 모듈 임포트
sys.path.append(os.getcwd())
from src.extractor import GeometryExtractor
from src.executor import SplitExecutor
from demo_full_pipeline import export_svg_views, generate_report_html, generate_report_md

def process_single_file(input_path, output_root, max_parts, min_volume):
    filename = os.path.basename(input_path)
    file_id = os.path.splitext(filename)[0]
    output_dir = os.path.join(output_root, file_id)
    
    print(f"\n--- 🚀 Processing: {filename} ---")
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    try:
        # 1. 모델 로드
        model = cq.importers.importStep(input_path)
        
        # 2. 형상 분석
        extractor = GeometryExtractor(model)
        summary = extractor.extract_summary()
        
        # 3. AI 전략 수립 (Ollama 연동)
        from src.planner import AIPlanner
        planner = AIPlanner()
        ai_plan = planner.plan_splits(summary)
        
        # 4. 시각화 (Before)
        before_views = export_svg_views(model, "before", output_dir)
        
        # 5. 분할 실행 (Executor)
        executor = SplitExecutor(model)
        solids = executor.execute_plan(ai_plan, max_parts=max_parts, min_volume_ratio=min_volume)
        
        # 6. 시각화 (After)
        combined_after = cq.Workplane("XY")
        for b in solids:
            combined_after = combined_after.add(b)
        after_views = export_svg_views(combined_after, "after", output_dir)
        
        # 7. 분할된 개별 솔리드들을 STEP 파일로 저장
        parts_dir = os.path.join(output_dir, "parts")
        os.makedirs(parts_dir, exist_ok=True)
        for i, solid in enumerate(solids):
            part_path = os.path.join(parts_dir, f"part_{i:02d}.step")
            cq.exporters.export(cq.Workplane(solid), part_path)
            
        # 8. 리포트 생성
        generate_report_html(output_dir, ai_plan, summary, before_views, after_views)
        generate_report_md(output_dir, ai_plan, summary)
        
        print(f"✅ Completed: {file_id}")
        
    except Exception as e:
        print(f"❌ Failed to process {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Batch AI Solid Decomposition Tool")
    parser.add_argument("--input_dir", default="input", help="Directory containing STEP files")
    parser.add_argument("--output_dir", default="output", help="Directory to save all results")
    parser.add_argument("--max-parts", type=int, default=15, help="Maximum number of split parts")
    parser.add_argument("--min-volume", type=float, default=0.01, help="Minimum volume ratio")
    args = parser.parse_args()

    # 입력 폴더 확인
    step_files = glob.glob(os.path.join(args.input_dir, "*.step")) + glob.glob(os.path.join(args.input_dir, "*.stp"))
    
    if not step_files:
        print(f"⚠️ No STEP files found in {args.input_dir}")
        return

    print(f"📦 Found {len(step_files)} files in '{args.input_dir}'. Starting batch processing...")
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for step_file in step_files:
        process_single_file(step_file, args.output_dir, args.max_parts, args.min_volume)

    print(f"\n✨ All batch tasks finished! Results are in '{args.output_dir}'")

if __name__ == "__main__":
    main()
