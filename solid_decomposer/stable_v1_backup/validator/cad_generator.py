import cadquery as cq
import os
import json
from feature_library import FeatureLibrary

class CADGenerator:
    def __init__(self, output_dir="validator/data"):
        self.output_dir = output_dir
        self.lib = FeatureLibrary()
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_final_boss(self):
        """[Lv.4 Super Compound] 모든 피쳐가 섞인 최종 보스 모델 생성"""
        print("🔥 Generating Lv.4 Final Boss Model (Robust Version)...")
        # 1. 몸체
        result = cq.Workplane("XY").box(150, 150, 60)
        
        # 2. 피쳐 A: 막힌 구멍 (Top)
        result = result.faces(">Z").workplane().circle(20).cutBlind(-40)
        
        # 3. 피쳐 B: 돌출 보스 (Side X)
        result = result.faces(">X").workplane().circle(25).extrude(30)
        
        # 4. 피쳐 C: 관통 구멍 (Side Y)
        result = result.faces(">Y").workplane().circle(15).cutThruAll()
        
        # 5. 피쳐 D: 필렛 추가 (구멍 모서리 생략하고 몸체 모서리에 추가하여 Transition 테스트)
        result = result.edges("|Z").fillet(3.0)
        
        features = [
            {"type": "Cylinder", "name": "BlindHole", "is_internal": True},
            {"type": "Cylinder", "name": "Boss", "is_internal": False},
            {"type": "Cylinder", "radius": 15, "is_internal": True}
        ]
        
        step_path = os.path.join(self.output_dir, "lv4_final_boss.step")
        cq.exporters.export(result, step_path)
        with open(os.path.join(self.output_dir, "lv4_final_boss_gt.json"), "w") as f:
            json.dump({"name": "lv4_final_boss", "expected_features": features}, f, indent=4)
        
        print(f"Final Boss model generated: {step_path}")
        return result

if __name__ == "__main__":
    gen = CADGenerator()
    gen.generate_final_boss()
