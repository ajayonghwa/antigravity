import os
import sys
import json

# 1~3단계 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '01_extractor'))
sys.path.append(os.path.join(os.path.dirname(__file__), '02_planner'))
sys.path.append(os.path.join(os.path.dirname(__file__), '03_generator'))

from extract_manager import ExtractManager
from strategy_planner import StrategyPlanner
from scdm_generator import SCDMGenerator

def run_pipeline(sub_device_name, input_json="geometry_data.json"):
    print(f"=== {sub_device_name} Solid Decomposition Pipeline Started ===")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(project_root, "data")
    script_dir = os.path.join(project_root, "04_scripts")
    
    # 1. 추출된 데이터 로드 (01_extractor)
    # 입력된 경로에서 파일명만 추출 (예: data/test.json -> test.json)
    input_filename = os.path.basename(input_json)
    manager = ExtractManager(project_root)
    data = manager.load_geometry_data(input_filename)
    
    if not data:
        print(f"Error: No data found for {input_json}. Please run scdm_extractor.py in SpaceClaim first.")
        return

    # 2. 분할 전략 수립 (02_planner)
    planner = StrategyPlanner(sub_device_name=sub_device_name)
    all_plans = []
    
    for body in data:
        print(f"\n[Analyzing Body: {body['body_name']}]")
        strategy, plans = planner.analyze_body(body)
        
        if plans:
            print(f" - Strategy: {strategy} ({len(plans)} plans)")
            all_plans.extend(plans)
        else:
            advice = planner.get_ai_advice(body)
            print(f" - AI Advice: {advice}")

    # 3. SCDM 실행 스크립트 생성 (03_generator)
    generator = SCDMGenerator(project_root)
    
    # 기기 이름이 들어간 유니크한 파일명 생성
    output_filename = f"{sub_device_name}_scdm_script.py"
    
    # 04_scripts 폴더 생성 확인
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
        
    # 직접 파일명을 전달하여 생성
    output_path = generator.generate_script(all_plans, output_name=output_filename)
    
    print(f"\n[Success] Final script generated: {output_path}")
    
    print(f"=== Pipeline Completed for {sub_device_name} ===")

if __name__ == "__main__":
    # 사용법: python main_run.py [기기이름] [입력파일]
    device = sys.argv[1] if len(sys.argv) > 1 else "TEST_DEVICE"
    input_file = sys.argv[2] if len(sys.argv) > 2 else "geometry_data.json"
    
    run_pipeline(device, input_file)
