import json
import os
import sys

# 프로젝트 루트 경로 추가 (상위 디렉토리)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 숫자로 시작하는 폴더명 대응
import importlib
planner_mod = importlib.import_module("02_planner.strategy_planner")
StrategyPlanner = planner_mod.StrategyPlanner

def run_virtual_validation():
    planner = StrategyPlanner(sub_device_name="VALVE_TEST")
    
    # 1. 다공 원판 (Lv.3) 검증
    with open("validator/data/auto_perforated_gt.json", "r") as f:
        gt_perforated = json.load(f)
    
    # 가상 바디 데이터 생성 (Extractor가 뽑았을 법한 형식으로 변환)
    mock_body_perf = {
        "body_name": "auto_perforated",
        "faces": [
            {"type": "Cylinder", "radius": 60.0, "axis": [0,0,1], "origin": [0,0,0], "box": {"min": [-60,-60,0], "max": [60,60,10]}}
        ]
    }
    # 구멍들 추가
    for i in range(6):
        mock_body_perf["faces"].append({"type": "Cylinder", "radius": 5.0, "axis": [0,0,1], "origin": [40,0,0], "box": {"min": [35,-5,0], "max": [45,5,10]}})

    print("=== Testing Planner with Perforated Disk (Lv.3) ===")
    strategy, plans = planner.analyze_body(mock_body_perf)
    print(f"Detected Strategy: {strategy}")
    print(f"Number of Split Plans: {len(plans)}")
    for p in plans:
        print(f" - {p['strategy']}: {p.get('core_offset', 'N/A')}")

    # 2. 휘어진 관 (Lv.9) 검증
    mock_body_curved = {
        "body_name": "auto_curved",
        "faces": [
            {"type": "Toroidal", "radius": 15.0, "origin": [50, 0, 50]}
        ]
    }
    
    print("\n=== Testing Planner with Curved Pipe (Lv.9) ===")
    strategy, plans = planner.analyze_body(mock_body_curved)
    print(f"Detected Strategy: {strategy}")
    print(f"Number of Split Plans: {len(plans)}")

if __name__ == "__main__":
    run_virtual_validation()
