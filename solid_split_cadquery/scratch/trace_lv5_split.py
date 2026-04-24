import cadquery as cq
from core.strategy_planner import StrategyPlanner
from core.classifier import Classifier
from core.splitter import Splitter
import os

model_path = "input/lv5_asymmetric_disk.step"
if os.path.exists(model_path):
    model = cq.importers.importStep(model_path)
    planner = StrategyPlanner(model)
    report = planner.classifier.get_feature_report()
    
    print("\n=== [lv5] 분할 과정 추적 ===")
    print(f"1. 감지된 특징 수: {len(report['features'])}")
    for f in report['features']:
        print(f"   - 타입: {f['type']}, 전략: {f['strategy']}, 반지름: {f['radius']}")
    
    # 실제 절단 시도 (O-GRID)
    active_bodies = [model]
    for feat in report['features']:
        if feat['strategy'] == "O-GRID":
            center = cq.Vector(*feat['centers'][0])
            radius = feat['radius']
            print(f"2. O-GRID 절단 시도: 중심={center}, 반지름={radius}")
            new_bodies = []
            for body in active_bodies:
                res = Splitter(body).apply_ogrid_split(center, radius, cq.Vector(0,0,1))
                print(f"   - 결과 조각 수: {len(res)}")
                new_bodies.extend(res)
            active_bodies = new_bodies

    print(f"3. 최종 바디 수: {len(active_bodies)}")
else:
    print("모델 파일을 찾을 수 없습니다.")
