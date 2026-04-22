import cadquery as cq
import os
import json

class CADGenerator:
    def __init__(self, output_dir="validator/data"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_asymmetric_disk(self):
        """[Lv.5 Challenge] 원판에 임의의 각도로 붙은 상자 2개 (30도, 120도)"""
        print("🌀 Generating Lv.5 Asymmetric Disk Challenge...")
        # 1. 메인 원판 (Disk)
        disk = cq.Workplane("XY").circle(60).extrude(15)
        
        # 2. 30도 위치의 상자
        box1 = (cq.Workplane("XY").workplane(offset=0)
                .center(0, 0).transformed(rotate=(0, 0, 30))
                .center(65, 0).box(20, 20, 30))
        
        # 3. 120도 위치의 상자
        box2 = (cq.Workplane("XY").workplane(offset=0)
                .center(0, 0).transformed(rotate=(0, 0, 120))
                .center(65, 0).box(15, 15, 30))
        
        result = disk.union(box1).union(box2)
        
        step_path = os.path.join(self.output_dir, "lv5_asymmetric_disk.step")
        cq.exporters.export(result, step_path)
        print(f"Asymmetric model generated: {step_path}")
        return result

if __name__ == "__main__":
    gen = CADGenerator()
    gen.generate_asymmetric_disk()
