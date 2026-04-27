import cadquery as cq
from core.strategy_planner import StrategyPlanner
from core.ai_planner import AIPlanner
import os

# 채점 로직 (batch_process_and_report에서 가져옴)
def score_body(body):
    faces = body.faces().vals()
    face_count = len(faces)
    if face_count == 6: return 100.0 # Perfect Box
    if face_count == 5: return 50.0  # Wedge/Prism
    if face_count <= 4: return 30.0  # Tet
    return max(0, 100 - (face_count - 6) * 5)

# 1. 모델 로드
model_path = "input/lv5_asymmetric_disk.step"
model = cq.importers.importStep(model_path)

# 2. AI 모드 플래너 생성
planner = StrategyPlanner(model, use_ai=True)

# 3. [AI 전략 주입] 제가 이 모델의 요약본을 보고 직접 수립한 계획입니다.
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

# 4. AI 계획 실행
print("\n--- 🤖 AI-Driven Decomposition & Scoring ---")
results = planner.plan_and_execute(ai_plan_json=ai_refined_strategy)

# 5. 채점 및 결과 출력
print(f"\n📊 [최종 결과] 생성된 조각: {len(results)}개")
total_score = 0
for i, b in enumerate(results):
    score = score_body(b)
    vol = b.val().Volume()
    total_score += score
    print(f"   [Body {i:02d}] 점수: {score:5.1f} | 부피: {vol:8.1f} | 면 개수: {len(b.faces().vals())}")

avg_score = total_score / len(results) if results else 0
print(f"\n✨ [평균 Hex Score] {avg_score:.2f}점")
