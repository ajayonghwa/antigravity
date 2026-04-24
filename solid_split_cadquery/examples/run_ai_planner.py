import cadquery as cq
from core.strategy_planner import StrategyPlanner
from core.ai_planner import AIPlanner
import json
import os

# 1. 모델 로드
model_path = "input/lv5_asymmetric_disk.step"
model = cq.importers.importStep(model_path)

# 2. AI 모드 플래너 생성
planner = StrategyPlanner(model, use_ai=True)

# 3. [AI 가상 개입] 제가 이 요약본을 보고 직접 쓴 '초정밀 전략' JSON입니다.
# 실제 환경에서는 제가 이 텍스트를 생성하여 시스템에 전달합니다.
ai_refined_strategy = """
{
    "overall_size": [129.95, 126.53, 30.0],
    "steps": [-15.0, 0.0, 15.0],
    "features": [
        {
            "type": "cylinder",
            "radius": 60.0,
            "centers": [[0.0, 0.0, 0.0]],
            "strategy": "O-GRID"
        }
    ],
    "main_axis": [0, 0, 1]
}
"""

# 4. AI 계획을 주입하여 실행
print("\n--- AI 기반 플래닝 모드 실행 ---")
results = planner.plan_and_execute(ai_plan_json=ai_refined_strategy)

print(f"\n✅ AI 분할 완료: 생성된 바디 수 = {len(results)}")
for i, b in enumerate(results):
    print(f"   [Body {i}] 부피: {b.val().Volume():.2f}")
