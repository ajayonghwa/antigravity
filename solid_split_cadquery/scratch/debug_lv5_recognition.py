import cadquery as cq
from core.classifier import Classifier
import json
import os

model_path = "input/lv5_asymmetric_disk.step"
if os.path.exists(model_path):
    model = cq.importers.importStep(model_path)
    classifier = Classifier(model)
    report = classifier.get_feature_report()
    
    print("\n=== [lv5_asymmetric_disk.step] 형상 인식 결과 ===")
    print(f"1. 전체 크기 (BBox): {report['overall_size']}")
    print(f"2. 감지된 단차 (Steps): {report['steps']}")
    print(f"3. 상세 특징 (Features):")
    for i, feat in enumerate(report['features']):
        print(f"   [{i}] 타입: {feat['type']}, 반지름: {feat['radius']:.2f}, 전략: {feat['strategy']}, 위치: {feat['centers'][0]}")
else:
    print("모델 파일을 찾을 수 없습니다.")
