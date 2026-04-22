import os
import sys
import json
import numpy as np

# 경로 추가
sys.path.append('solid_decomposer/02_planner')
sys.path.append('solid_decomposer/03_generator')
sys.path.append('solid_decomposer')

from strategy_planner import StrategyPlanner
from scdm_generator import SCDMGenerator
from scdm_bridge.guide_generator import GuideGenerator

def debug_run():
    print("🐞 Starting Deep Debug of Pipeline...")
    
    # 1. 모의 데이터 생성 (원기둥 + 상자 조합)
    mock_body = {
        "body_name": "Debug_Cylinder",
        "faces": [
            {"type": "Cylinder", "radius": 40, "origin": [0,0,50], "axis": [0,0,1], "is_internal": False, "box": {"min": [-40,-40,0], "max": [40,40,100]}},
            {"type": "Plane", "normal": [0,0,1], "origin": [0,0,100], "box": {"min": [-40,-40,100], "max": [40,40,100]}},
            {"type": "Plane", "normal": [0,0,1], "origin": [0,0,0], "box": {"min": [-40,-40,0], "max": [40,40,0]}}
        ]
    }
    
    # 2. 플래너 실행
    planner = StrategyPlanner(sub_device_name="DEBUG_RUN")
    strategy, plans = planner.analyze_body(mock_body)
    
    print(f"\n[Planner Output]")
    print(f"Overall Strategy: {strategy}")
    print(f"Number of Plans: {len(plans)}")
    
    for i, p in enumerate(plans):
        print(f"Step {i+1}: {p['strategy']}")
        # 데이터 타입 확인 (가장 중요!)
        if 'center' in p: print(f" - Center Type: {type(p['center'])}")
        if 'split_plane' in p: print(f" - Normal Type: {type(p['split_plane']['normal'])}")

    # 3. 가이드 생성기 테스트
    print("\n[Guide Generator Test]")
    guide_md = GuideGenerator.generate_markdown("Debug_Cylinder", strategy, plans)
    print("--- Guide Content Start ---")
    print(guide_md)
    print("--- Guide Content End ---")

    # 4. 스크립트 생성기 테스트
    print("\n[Script Generator Test]")
    gen = SCDMGenerator(os.getcwd())
    # 임시 파일로 생성
    output_path = gen.generate_script(plans, "debug_scdm_script.py")
    with open(output_path, "r", encoding="utf-8") as f:
        print("--- Script Content Start ---")
        print(f.read())
        print("--- Script Content End ---")

if __name__ == "__main__":
    debug_run()
