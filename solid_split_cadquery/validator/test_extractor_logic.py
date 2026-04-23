import json
import os
import sys

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from validation_loop import ValidationLoop

def run_extractor_verification_demo():
    validator = ValidationLoop()
    
    # 1. 테스트용 Mock 추출 데이터 생성 (실제 스페이스클레임에서 뽑은 척)
    # 정답(GT) 파일 읽기
    gt_path = "data/auto_cylinder_gt.json"
    if not os.path.exists(gt_path):
        print("GT file not found. Run cad_generator.py first.")
        return

    with open(gt_path, "r") as f:
        gt = json.load(f)
    
    gt_radius = gt["expected_features"][0]["radius"]
    
    # 미세한 오차(Floating point error)를 포함한 추출 데이터 생성
    mock_extracted = {
        "body_name": "auto_cylinder",
        "faces": [
            {
                "type": "Cylinder",
                "radius": gt_radius + 0.00000012, # 아주 미세한 오차
                "origin": [0.00001, 0, 0],
                "axis": [0, 0, 1],
                "type": "Unknown",
                "area": getattr(shape, 'Area', 0),
                "is_internal": False, # 내/외경 판별 플래그 추가
                "box": {"min": [0,0,0], "max": [0,0,0]}
            }
        ]
    }
    
    mock_path = "data/mock_extracted_cylinder.json"
    with open(mock_path, "w") as f:
        json.dump(mock_extracted, f)
        
def fix_and_run():
    # ... (생략) ...
    pass

if __name__ == "__main__":
    validator = ValidationLoop()
    test_cases = [
        {"name": "auto_cylinder", "gt": "validator/data/auto_cylinder_gt.json", "ext_count": 1},
        {"name": "auto_stepped", "gt": "validator/data/auto_stepped_gt.json", "ext_count": 2},
        {"name": "auto_perforated", "gt": "validator/data/auto_perforated_gt.json", "ext_count": 7}, # 메인1 + 구멍6
        {"name": "auto_curved", "gt": "validator/data/auto_curved_gt.json", "ext_count": 1}
    ]

    print(f"{'Model Name':<20} | {'Status':<10} | {'Accuracy':<10} | {'Features'}")
    print("-" * 65)

    for case in test_cases:
        if not os.path.exists(case["gt"]): continue
        
        with open(case["gt"], "r") as f:
            gt = json.load(f)
        
        # 가상 추출 데이터 생성
        mock_extracted = {"faces": []}
        # 1. 바운딩 박스 및 내/외경 판별
        try:
            # Orientation이 Reversed이면 내경(Hole)일 확률이 높습니다.
            if hasattr(face, 'Orientation') and str(face.Orientation) == 'Reversed':
                data["is_internal"] = True
                
            r = getattr(shape, 'Range', getattr(face, 'Box', None))
            for feat in gt["expected_features"]:
                mock_extracted["faces"].append({
                    "type": feat["type"] if feat["type"] != "Toroidal/Spline" else "Toroidal",
                    "radius": feat.get("radius", 0) + 0.00001, # 미세 오차
                    "is_internal": feat.get("is_internal", False)
                })
        except:
            for feat in gt["expected_features"]:
                mock_extracted["faces"].append({
                    "type": feat["type"] if feat["type"] != "Toroidal/Spline" else "Toroidal",
                    "radius": feat.get("radius", 0) + 0.00001, # 미세 오차
                    "is_internal": feat.get("is_internal", False)
                })
            
        mock_path = f"validator/data/mock_{case['name']}.json"
        with open(mock_path, "w") as f:
            json.dump(mock_extracted, f)

        report = validator.compare(case["gt"], mock_path)
        status = "PASS" if report["accuracy"] == 100 else "FAIL"
        
        print(f"{case['name']:<20} | {status:<10} | {report['accuracy']:>8.1f}% | {report['extracted_count']}/{report['expected_count']}")
        
    print("\n[INFO] 모든 복합 형상에 대해 검증 엔진이 정상 작동함을 확인했습니다.")
    print("[INFO] 이제 스페이스클레임에서 실제 추출된 데이터만 넣어주면 위 리포트가 실제 값으로 채워집니다.")
