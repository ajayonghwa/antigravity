import cadquery as cq
from core.strategy_planner import StrategyPlanner
import os

model_path = "input/edge_perforated.step"
if os.path.exists(model_path):
    model = cq.importers.importStep(model_path)
    orig_vol = model.val().Volume()
    
    planner = StrategyPlanner(model)
    results = planner.plan_and_execute()
    
    final_vol = sum(b.val().Volume() for b in results)
    loss = orig_vol - final_vol
    loss_percent = (loss / orig_vol) * 100
    
    print(f"\n=== [edge_perforated.step] 부피 점검 결과 ===")
    print(f"1. 원본 부피: {orig_vol:.6f}")
    print(f"2. 분할 후 합계 부피: {final_vol:.6f}")
    print(f"3. 손실된 부피: {loss:.6f} ({loss_percent:.4f}%)")
    print(f"4. 생성된 바디 수: {len(results)}")
    
    if abs(loss_percent) > 0.1:
        print("\n⚠️ 경고: 유의미한 부피 소실이 감지되었습니다!")
    else:
        print("\n✅ 통과: 부피가 안정적으로 보존되었습니다.")
else:
    print("모델 파일을 찾을 수 없습니다.")
