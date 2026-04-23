import os
import cadquery as cq
from core.splitter import Splitter
from validator.engine import ValidationEngine

def gemini_expert_split():
    validator = ValidationEngine()
    input_dir = "input"
    
    # 1. LV4 FINAL BOSS 
    print("\n--- Processing LV4 FINAL BOSS (Expert Mode) ---")
    model = cq.importers.importStep(os.path.join(input_dir, "lv4_final_boss.step"))
    
    # [Expert Strategy]
    s1 = Splitter(model)
    # Step 1: Detach Boss
    bodies = s1.apply_planar_split(cq.Vector(50, 0, 0), cq.Vector(1, 0, 0))
    
    final_bodies = []
    for b in bodies:
        s = Splitter(b)
        bbox = b.val().BoundingBox()
        if bbox.center.x > 50: # This is the Boss
            # Step 2: O-Grid on Boss Hole (X=70, Axis=Z)
            b_split = s.apply_ogrid(cq.Vector(70, 0, 0), cq.Vector(0, 0, 1), radius=15)
            # Step 3: Transverse split on Boss
            for part in b_split:
                final_bodies.extend(Splitter(part).apply_planar_split(cq.Vector(70, 0, 0), cq.Vector(1, 0, 0)))
        else: # This is the Main Block
            # Step 4: O-Grid on Top Blind Hole (X=0, Y=0, Axis=Z)
            b_split = s.apply_ogrid(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), radius=20)
            # Step 5: Horizontal cut at blind hole bottom (Z=30)
            for part in b_split:
                final_bodies.extend(Splitter(part).apply_planar_split(cq.Vector(0, 0, 30), cq.Vector(0, 0, 1)))

    res = validator.validate_split(model, final_bodies)
    print(f"🏆 Gemini Expert Score: {res['hex_readiness']['average_score']:.1f}")
    
    # 2. PARTITIONED CYLINDER
    print("\n--- Processing PARTITIONED CYLINDER (Expert Mode) ---")
    model2 = cq.importers.importStep(os.path.join(input_dir, "partitioned_cylinder.step"))
    # Step 1: Split at Z=70 (Top of partition)
    bodies2 = Splitter(model2).apply_planar_split(cq.Vector(0, 0, 70), cq.Vector(0, 0, 1))
    final_bodies2 = []
    for b in bodies2:
        # Step 2: Split at Z=60 (Bottom of partition)
        final_bodies2.extend(Splitter(b).apply_planar_split(cq.Vector(0, 0, 60), cq.Vector(0, 0, 1)))
        
    res2 = validator.validate_split(model2, final_bodies2)
    print(f"🏆 Gemini Expert Score: {res2['hex_readiness']['average_score']:.1f}")

if __name__ == "__main__":
    gemini_expert_split()
