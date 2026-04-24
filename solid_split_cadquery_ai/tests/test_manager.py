import cadquery as cq
import json
import os
import sys
import time
import numpy as np
from typing import List, Dict, Any

# Add src to path to import extractor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.extractor import GeometryExtractor

class TestManager:
    def __init__(self):
        self.results = []

    def create_simple_box(self) -> cq.Workplane:
        return cq.Workplane("XY").box(100, 100, 10)

    def create_simple_cylinder(self) -> cq.Workplane:
        return cq.Workplane("XY").cylinder(50, 20)

    def create_plate_with_holes(self, count=4, radius=5) -> cq.Workplane:
        plate = cq.Workplane("XY").box(100, 100, 10)
        if count == 4:
            locs = [(25, 25), (25, -25), (-25, 25), (-25, -25)]
            for loc in locs:
                plate = plate.faces(">Z").workplane().move(*loc).hole(radius*2)
        return plate

    def create_stepped_hole(self) -> cq.Workplane:
        block = cq.Workplane("XY").box(100, 100, 20)
        block = block.faces(">Z").workplane().hole(20, 10)
        block = block.faces(">Z").workplane().hole(10)
        return block

    def create_composite_shape(self) -> cq.Workplane:
        base = cq.Workplane("XY").cylinder(20, 20)
        block = cq.Workplane("XY").rect(10, 10).extrude(30).translate((20, 0, 0))
        return base.union(block)

    def create_stepped_shaft(self) -> cq.Workplane:
        result = cq.Workplane("XY").circle(20).extrude(20)\
                 .faces(">Z").workplane().circle(15).extrude(20)\
                 .faces(">Z").workplane().circle(10).extrude(20)
        return result

    def create_hollow_cylinder(self) -> cq.Workplane:
        return cq.Workplane("XY").circle(20).extrude(50).faces(">Z").workplane().hole(20)

    def create_gear_simple(self) -> cq.Workplane:
        base = cq.Workplane("XY").cylinder(20, 20)
        for angle in [0, 90, 180, 270]:
            tooth = cq.Workplane("XY").rect(5, 10).extrude(20).translate((22, 0, 0)).rotate((0,0,0), (0,0,1), angle)
            base = base.union(tooth)
        return base

    def create_mid_disk_cylinder(self) -> cq.Workplane:
        cyl = cq.Workplane("XY").cylinder(100, 10)
        disk = cq.Workplane("XY").circle(30).extrude(10).translate((0,0,-5))
        return cyl.union(disk)

    def create_stepped_section_disk(self) -> cq.Workplane:
        return cq.Workplane("XY").circle(40).extrude(10)\
                 .faces(">Z").workplane().circle(30).extrude(10)\
                 .faces(">Z").workplane().circle(20).extrude(10)

    def create_flanged_tube(self) -> cq.Workplane:
        tube = cq.Workplane("XY").circle(20).extrude(60).faces(">Z").workplane().hole(30)
        flange = cq.Workplane("XY").circle(40).extrude(10)
        return tube.union(flange)

    def create_t_junction(self) -> cq.Workplane:
        main = cq.Workplane("XY").cylinder(100, 20)
        branch = cq.Workplane("XZ").cylinder(80, 15)
        return main.union(branch)

    def create_slotted_block(self) -> cq.Workplane:
        return cq.Workplane("XY").box(100, 100, 20).faces(">Z").workplane().rect(60, 20).cutBlind(-10)

    def run_test(self, name: str, model_gen_func, expected_feature_types: List[str]):
        print(f"--- Running Test: {name} ---")
        try:
            model = model_gen_func()
            extractor = GeometryExtractor(model)
            summary = extractor.extract_summary()
            
            detected_types = [f["type"] for f in summary["features"]]
            
            success = True
            for expected in expected_feature_types:
                if expected not in detected_types:
                    print(f"❌ Missing expected feature type: {expected}")
                    success = False
            
            if success:
                print(f"✅ Test Passed: {name}")
            else:
                print(f"❌ Test Failed: {name}")
                print(f"Summary: {json.dumps(summary, indent=2)}")
            
            self.results.append({
                "name": name,
                "success": success,
                "summary": summary
            })
            return success
        except Exception as e:
            print(f"💥 Test Errored: {name} - {e}")
            self.results.append({"name": name, "success": False, "error": str(e)})
            return False

    def run_all(self):
        start_time = time.time()
        
        # Original Test Cases
        self.run_test("Simple Box", self.create_simple_box, [])
        self.run_test("Simple Cylinder", self.create_simple_cylinder, ["cylinder"])
        self.run_test("Plate with 4 Holes", lambda: self.create_plate_with_holes(4, 5), ["hole"])
        self.run_test("Stepped Hole", self.create_stepped_hole, ["stepped_hole"])
        self.run_test("Composite Shape", self.create_composite_shape, ["cylinder", "junction"])
        self.run_test("Stepped Shaft", self.create_stepped_shaft, ["stepped_shaft"])
        self.run_test("Hollow Cylinder", self.create_hollow_cylinder, ["tube"])
        self.run_test("Gear Simple", self.create_gear_simple, ["cylinder", "junction"])
        
        # New Complex Test Cases
        self.run_test("Mid-Disk Cylinder", self.create_mid_disk_cylinder, ["stepped_shaft", "junction"])
        self.run_test("Stepped Section Disk", self.create_stepped_section_disk, ["stepped_shaft"])
        self.run_test("Flanged Tube", self.create_flanged_tube, ["stepped_tube", "junction"])
        self.run_test("T-Junction", self.create_t_junction, ["cylinder", "junction"])
        self.run_test("Slotted Block", self.create_slotted_block, ["junction"])

        end_time = time.time()
        print(f"\nTotal Time: {end_time - start_time:.2f}s")
        self.print_report()

    def print_report(self):
        passed = sum(1 for r in self.results if r.get("success", False))
        total = len(self.results)
        print(f"\nFinal Report: {passed}/{total} tests passed.")

if __name__ == "__main__":
    manager = TestManager()
    manager.run_all()
