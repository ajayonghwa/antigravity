import cadquery as cq
import os
import sys

# 프로젝트 루트를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.strategy_planner import StrategyPlanner
from validator.engine import ValidationEngine

def debug_single_file(file_name):
    file_path = os.path.join("input", file_name)
    print(f"🔍 Debugging {file_name}...")
    
    model = cq.importers.importStep(file_path)
    planner = StrategyPlanner(model)
    
    print(f"📊 Global Report Holes: {len(planner.global_report['holes'])}")
    for i, hole in enumerate(planner.global_report['holes']):
        print(f"   Hole {i}: Center={hole['center']}, R={hole.get('radius')}")
    
    results = planner.plan_and_execute()
    print(f"✅ Final Bodies: {len(results)}")
    
    validator = ValidationEngine()
    total_score = validator.calculate_hex_readiness(results)
    print(f"📈 Final Score: {total_score:.2f}")

if __name__ == "__main__":
    debug_single_file("perforated_2x4_s40_r10.step")
