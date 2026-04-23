# -*- coding: utf-8 -*-
import os
import sys
import json
import traceback

def run_pipeline(sub_device_name, input_json="geometry_data.json"):
    print(f"=== {sub_device_name} Solid Decomposition Pipeline Started (v4.54) ===")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # [v4.54] 임포트 로직을 try 블록 내부로 이동 (ModuleNotFoundError 추적용)
        print(" - Loading internal modules...")
        sys.path.append(os.path.join(project_root, '01_extractor'))
        sys.path.append(os.path.join(project_root, '02_planner'))
        sys.path.append(os.path.join(project_root, '03_generator'))
        sys.path.append(os.path.join(project_root, 'scdm_bridge'))

        try:
            from extract_manager import ExtractManager
            from strategy_planner import StrategyPlanner
            from scdm_generator import SCDMGenerator
            from guide_generator import GuideGenerator
            import numpy as np
            print("   [OK] All modules loaded (including numpy)")
        except ImportError as ie:
            print(f"\n[CRITICAL ERROR] Dependency Missing: {str(ie)}")
            print("Please ensure 'numpy' is installed in your python environment.")
            sys.exit(1)

        # 1. 추출된 데이터 로드
        input_filename = os.path.basename(input_json)
        manager = ExtractManager(project_root)
        data = manager.load_geometry_data(input_filename)
        
        if not data:
            print(f"[ERROR] No data found for {input_json}.")
            return

        # 2. 분할 전략 수립
        planner = StrategyPlanner(sub_device_name=sub_device_name)
        all_plans = []
        
        bodies_list = data.get("bodies", [])
        current_units = data.get("units", "m")
        print(f" - Model Units: {current_units} | Found {len(bodies_list)} bodies")

        for body in bodies_list:
            b_name = body.get('body_name', 'Unknown')
            print(f"\n[Analyzing Body: {b_name}]")
            try:
                strategy, plans = planner.analyze_body(body, units=current_units)
                if plans:
                    print(f"   [OK] Strategy: {strategy} ({len(plans)} plans)")
                    all_plans.extend(plans)
                else:
                    print(f"   [SKIP] No automatic plans generated.")
            except Exception as e:
                print(f"   [CRASH] Error during analysis: {str(e)}")
                traceback.print_exc()

        # 3. SCDM 실행 스크립트 생성
        generator = SCDMGenerator(project_root)
        output_filename = "scdm_decomposition_script.py"
        output_path = generator.generate_script(all_plans, output_name=output_filename)
        print(f"\n[Success] Step 3 script generated: {output_path}")
        
        # 4. 분석 결과 리포트(MD) 생성
        try:
            guide_text = f"# Decomposition Strategy Report: {sub_device_name}\n"
            guide_text += f"- **Model Units**: {current_units}\n\n"
            for body in bodies_list:
                strategy, plans = planner.analyze_body(body)
                guide_text += GuideGenerator.generate_markdown(body.get('body_name','Unknown'), strategy, plans)
                guide_text += "\n\n"
            guide_path = os.path.join(project_root, "04_scripts", "Decomposition_Guide.md")
            with open(guide_path, "w", encoding="utf-8") as f: f.write(guide_text)
            print(f"[Success] Planning guide generated: {guide_path}")
        except Exception as ge:
            print(f" [WARN] Guide generation failed: {str(ge)}")

        print(f"\n=== Pipeline Completed for {sub_device_name} ===")

    except Exception as e:
        print(f"\n[FATAL ERROR] Pipeline failed: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    device = sys.argv[1] if len(sys.argv) > 1 else "TEST_DEVICE"
    input_file = sys.argv[2] if len(sys.argv) > 2 else "geometry_data.json"
    run_pipeline(device, input_file)
