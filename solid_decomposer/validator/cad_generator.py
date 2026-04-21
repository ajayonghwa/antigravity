import cadquery as cq
import json
import os
import random

class CADGenerator:
    """
    CadQuery를 이용해 무작위 STEP 파일과 정답지(JSON)를 생성하는 모듈.
    """
    def __init__(self, output_dir="validator/data"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_test_case(self, level=1, name="test_model"):
        if level == 1:
            return self._generate_lv1_cylinder(name)
        elif level == 2:
            return self._generate_lv2_stepped(name)
        elif level == 3:
            return self._generate_lv3_perforated_disk(name)
        elif level == 9:
            return self._generate_lv9_curved_pipe(name)
        return None

    def _generate_lv1_cylinder(self, name):
        radius = round(random.uniform(10, 40), 2)
        height = round(random.uniform(50, 100), 2)
        
        # CadQuery 모델 생성
        result = cq.Workplane("XY").circle(radius).extrude(height)
        
        # 파일 저장
        step_path = os.path.join(self.output_dir, f"{name}.step")
        cq.exporters.export(result, step_path)
        
        # 정답지(Ground Truth) 저장
        gt_data = {
            "name": name,
            "level": 1,
            "expected_features": [
                {"type": "Cylinder", "radius": radius, "height": height, "axis": [0,0,1]}
            ]
        }
        gt_path = os.path.join(self.output_dir, f"{name}_gt.json")
        with open(gt_path, "w", encoding="utf-8") as f:
            json.dump(gt_data, f, indent=4)
            
        return step_path, gt_path

    def _generate_lv2_stepped(self, name):
        r1 = round(random.uniform(30, 40), 2)
        r2 = round(random.uniform(15, 25), 2)
        h1 = round(random.uniform(30, 50), 2)
        h2 = round(random.uniform(30, 50), 2)
        
        # 2단 실린더 생성
        result = (cq.Workplane("XY")
                  .circle(r1).extrude(h1)
                  .faces(">Z").workplane()
                  .circle(r2).extrude(h2))
        
        step_path = os.path.join(self.output_dir, f"{name}.step")
        cq.exporters.export(result, step_path)
        
        gt_data = {
            "name": name,
            "level": 2,
            "expected_features": [
                {"type": "Cylinder", "radius": r1, "height": h1, "origin": [0,0,0]},
                {"type": "Cylinder", "radius": r2, "height": h2, "origin": [0,0,h1]}
            ]
        }
        gt_path = os.path.join(self.output_dir, f"{name}_gt.json")
        with open(gt_path, "w", encoding="utf-8") as f:
            json.dump(gt_data, f, indent=4)
            
        return step_path, gt_path

    def _generate_lv3_perforated_disk(self, name):
        outer_r = 60.0
        thick = 10.0
        num_holes = 6
        hole_r = 5.0
        dist = 40.0
        
        # 메인 원판
        result = cq.Workplane("XY").circle(outer_r).extrude(thick)
        
        # 구멍 뚫기 (polarArray 사용하여 정확하게 배치)
        result = (result.faces(">Z").workplane()
                  .polarArray(radius=dist, startAngle=0, angle=360, count=num_holes)
                  .circle(hole_r).cutThruAll())
        
        step_path = os.path.join(self.output_dir, f"{name}.step")
        cq.exporters.export(result, step_path)
        
        gt_data = {
            "name": name, "level": 3,
            "expected_features": [{"type": "Cylinder", "radius": outer_r, "role": "Main"}] + 
                                [{"type": "Cylinder", "radius": hole_r, "role": "Hole"} for _ in range(num_holes)]
        }
        gt_path = os.path.join(self.output_dir, f"{name}_gt.json")
        with open(gt_path, "w", encoding="utf-8") as f:
            json.dump(gt_data, f, indent=4)
        return step_path, gt_path

    def _generate_lv9_curved_pipe(self, name):
        # 속이 뻥 뚫린 이중 파이프 (내외경 판별 완벽 증명용)
        outer_r = 20.0
        inner_r = 10.0
        height = 100.0
        result = (cq.Workplane("XY")
                  .circle(outer_r).circle(inner_r) # 두 개의 원을 그리면 자동으로 속이 빔
                  .extrude(height))
        
        step_path = os.path.join(self.output_dir, f"{name}.step")
        cq.exporters.export(result, step_path)
        
        gt_data = {
            "name": name, "level": 9,
            "expected_features": [{"type": "Cylinder", "radius": outer_r, "is_internal": False},
                                 {"type": "Cylinder", "radius": inner_r, "is_internal": True}]
        }
        gt_path = os.path.join(self.output_dir, f"{name}_gt.json")
        with open(gt_path, "w", encoding="utf-8") as f:
            json.dump(gt_data, f, indent=4)
        return step_path, gt_path

if __name__ == "__main__":
    gen = CADGenerator()
    gen.generate_test_case(1, "auto_cylinder")
    gen.generate_test_case(2, "auto_stepped")
    gen.generate_test_case(3, "auto_perforated")
    gen.generate_test_case(9, "auto_curved")
    print("Test models (Cylinder, Stepped, Perforated, Curved) generated.")
