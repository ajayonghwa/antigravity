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
        """[Lv.4 Super Compound] 사각 블록 + 옆면 원기둥 + 간섭 없는 관통공"""
        print("🔥 Generating Refined Lv.4 Final Boss Model (Correct Paths)...")
        
        # 프로젝트 루트 경로 찾기
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # 1. 메인 사각 블록 (100x100x50, 중심 0,0,0)
        result = cq.Workplane("XY").box(100, 100, 50)
        
        # 2. 피쳐 A: 옆면 돌출 원기둥 (Side X)
        # 사각 블록 옆면(X=50)에 반경 20(지름 40) 원기둥을 40만큼 돌출
        result = result.faces(">X").workplane().circle(20).extrude(40)
        
        # 3. 피쳐 B: 원기둥만 관통하는 구멍 (사각 블록 간섭 회피)
        # 원기둥은 X=50~90에 위치. X=70 지점에서 구멍 생성
        result = (result.faces(">Z").workplane(offset=0, origin=(70, 0, 0))
                  .circle(10).cutThruAll())
        
        # 4. 피쳐 C: 상단 막힌 구멍 (Top)
        result = result.faces(">Z").workplane(origin=(0, 0, 0)).circle(15).cutBlind(-20)
        
        # 5. 피쳐 D: 필렛
        result = result.edges("|Z").fillet(2.0)
        
        # 파일 저장 (절대 경로 사용)
        step_name = "lv4_final_boss.step"
        validator_data_path = os.path.join(project_root, self.output_dir, step_name)
        input_folder_path = os.path.join(project_root, "input", step_name)
        
        cq.exporters.export(result, validator_data_path)
        cq.exporters.export(result, input_folder_path)
        
        with open(os.path.join(project_root, self.output_dir, "lv4_final_boss_gt.json"), "w") as f:
            json.dump({"name": "lv4_final_boss", "expected_features": []}, f, indent=4)
        
        print(f"✅ Success: Saved to {input_folder_path}")
        return result

    def generate_custom_perforated_plate(self, rows=3, cols=3, spacing=30, hole_radius=8):
        """다양한 구멍 크기와 간격을 가진 동적 다공판 생성"""
        print(f"🧩 Generating Custom Perforated Plate ({rows}x{cols})...")
        width = cols * spacing + spacing
        height = rows * spacing + spacing
        plate = cq.Workplane("XY").box(width, height, 10)
        for r in range(rows):
            for c in range(cols):
                x = (c - (cols-1)/2) * spacing
                y = (r - (rows-1)/2) * spacing
                plate = plate.faces(">Z").workplane().center(x, y).circle(hole_radius).cutThruAll()
        name = f"perforated_{rows}x{cols}_s{spacing}_r{hole_radius}.step"
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        path = os.path.join(project_root, "input", name)
        cq.exporters.export(plate, path)
        return plate

    def generate_edge_perforated_plate(self):
        """경계면에 구멍이 쏠린 불규칙 다공판"""
        print("🧩 Generating Edge Perforated Plate...")
        plate = cq.Workplane("XY").box(100, 100, 10)
        # 경계면 근처 구멍들
        coords = [(40, 40), (-40, -40), (40, -40), (0, 42)] 
        for x, y in coords:
            plate = plate.faces(">Z").workplane().center(x, y).circle(6).cutThruAll()
        
        path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "input", "edge_perforated.step")
        cq.exporters.export(plate, path)
        return plate

    def generate_partitioned_cylinder(self):
        """내부에 격벽이 있는 원통 (Partitioned Cylinder)"""
        print("🧩 Generating Partitioned Cylinder...")
        # 외경 40, 높이 100 원통
        cyl = cq.Workplane("XY").circle(20).extrude(100)
        # 내부에 두 개의 원판 파티션 (Z=30, Z=70)
        # 사실 파티션을 만들려면 내부를 파내고 판을 남겨야 함
        cyl = cyl.faces(">Z").workplane(offset=-30).circle(20).split(keepTop=True, keepBottom=True)
        # CadQuery에서 내부 파티션은 복합 바디로 표현되거나 cut으로 생성
        # 여기서는 단순화를 위해 가운데가 뚫린 원통에 판이 끼워진 형상을 모사
        result = cq.Workplane("XY").circle(20).extrude(100).faces(">Z").workplane(offset=-30).rect(40,40).cutBlind(-10)
        
        path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "input", "partitioned_cylinder.step")
        cq.exporters.export(result, path)
        return result

    def generate_offset_perforated_plate(self):
        """원점에서 멀리 떨어진 미지의 다공판 (테스트용)"""
        print("🧩 Generating Offset Perforated Plate (Testing Origin Independence)...")
        # 원점에서 (150, 150) 만큼 떨어진 곳에 생성
        plate = cq.Workplane("XY").workplane(offset=50).center(150, 150).box(80, 80, 10)
        # 구멍 4개 생성
        for x, y in [(20, 20), (-20, -20), (20, -20), (-20, 20)]:
            plate = plate.faces(">Z").workplane().center(x, y).circle(5).cutThruAll()
        
        path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "input", "mystery_offset_plate.step")
        cq.exporters.export(plate, path)
        return plate

    def generate_elbow(self):
        """곡면 엘보우 파이프 (스윕 경로 분할 테스트용)"""
        print("🧩 Generating Elbow Pipe...")
        # 90도 꺾인 경로 생성
        path = cq.Workplane("XZ").moveTo(50, 0).radiusArc((0, 50), 50)
        result = cq.Workplane("XY").circle(15).sweep(path)
        
        save_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "input", "complex_elbow.step")
        cq.exporters.export(result, save_path)
        return result

    def generate_stepped_disk(self):
        """3단 단차 원판 (섹터 분할 테스트용)"""
        print("🧩 Generating Stepped Disk...")
        result = cq.Workplane("XY").circle(40).extrude(20)\
                 .faces(">Z").workplane().circle(25).extrude(20)\
                 .faces(">Z").workplane().circle(15).extrude(20)
        
        save_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "input", "complex_stepped_disk.step")
        cq.exporters.export(result, save_path)
        return result

    def generate_cross_hole(self):
        """교차 구멍 블록 (45도 회전 분할 테스트용)"""
        print("🧩 Generating Cross-Hole Block...")
        block = cq.Workplane("XY").box(60, 60, 60)
        # X축 관통 구멍
        block = block.faces(">X").workplane().circle(10).cutThruAll()
        # Y축 관통 구멍 (내부에서 X축 구멍과 교차)
        block = block.faces(">Y").workplane().circle(10).cutThruAll()
        
        save_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "input", "complex_cross_hole.step")
        cq.exporters.export(block, save_path)
        return block

if __name__ == "__main__":
    gen = CADGenerator()
    gen.generate_final_boss()
    gen.generate_custom_perforated_plate(rows=2, cols=4, spacing=40, hole_radius=10)
    gen.generate_edge_perforated_plate()
    gen.generate_partitioned_cylinder()
    gen.generate_offset_perforated_plate()
    gen.generate_elbow()
    gen.generate_stepped_disk()
    gen.generate_cross_hole()
