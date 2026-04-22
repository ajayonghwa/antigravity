import json
import os

class ValidationLoop:
    """
    추출된 데이터(Extracted)와 정답지(Ground Truth)를 비교하여 시스템 신뢰도를 채점하는 모듈.
    """
    def compare(self, gt_path, extracted_path):
        with open(gt_path, "r", encoding="utf-8") as f:
            gt = json.load(f)
        
        if not os.path.exists(extracted_path):
            return {"status": "FAIL", "reason": "Extracted file not found"}

        with open(extracted_path, "r", encoding="utf-8") as f:
            extracted = json.load(f)

        results = {
            "model_name": gt["name"],
            "level": gt["level"],
            "expected_count": len(gt["expected_features"]),
            "extracted_count": len(extracted.get("faces", [])),
            "errors": []
        }

        # 간단한 매칭 테스트 (타입 별칭 및 반지름 비교)
        match_count = 0
        type_aliases = {
            "Toroidal/Spline": "Toroidal",
            "Cylinder": "Cylinder"
        }

        for exp in gt["expected_features"]:
            found = False
            exp_type = type_aliases.get(exp["type"], exp["type"])
            
            for ext in extracted.get("faces", []):
                ext_type = type_aliases.get(ext["type"], ext["type"])
                
                if ext_type == exp_type:
                    # 반지름 비교 (0.1mm 오차 허용)
                    radius_match = abs(ext.get("radius", 0) - exp.get("radius", 0)) < 0.1
                    # 내/외경 일치 여부 (있을 경우에만 체크)
                    internal_match = True
                    if "is_internal" in ext and "is_internal" in exp:
                        internal_match = (ext["is_internal"] == exp["is_internal"])
                        
                    if radius_match and internal_match:
                        found = True
                        match_count += 1
                        break
            if not found:
                results["errors"].append(f"Missing feature: {exp['type']} (Radius: {exp.get('radius')})")

        results["accuracy"] = (match_count / results["expected_count"]) * 100 if results["expected_count"] > 0 else 0
        return results

if __name__ == "__main__":
    # 사용 예시
    validator = ValidationLoop()
    # 실제 사용 시에는 스페이스클레임에서 추출된 JSON 경로를 넣어야 함
    # res = validator.compare("validator/data/auto_stepped_gt.json", "data/extracted_stepped.json")
    # print(json.dumps(res, indent=4))
    print("Validation Loop ready. Please run this after extracting data in SpaceClaim.")
