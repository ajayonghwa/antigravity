import os
import cadquery as cq
from core.splitter import Splitter
from validator.engine import ValidationEngine

def gemini_perfect_split():
    validator = ValidationEngine()
    input_dir = "input"
    
    # --- 1. AUTO CYLINDER (Perfect 5-Body Hex) ---
    print("\n💎 [Expert] Processing AUTO CYLINDER...")
    model = cq.importers.importStep(os.path.join(input_dir, "auto_cylinder.step"))
    s = Splitter(model)
    # Core-Shell O-Grid
    bodies = s.apply_ogrid(cq.Vector(0,0,0), cq.Vector(0,0,1), radius=10) # radius 10 for 20 radius cyl
    final_cylinder = []
    for b in bodies:
        if b.val().Volume() < 5000: # Core (Approx)
            final_cylinder.append(b)
        else: # Shell - Split into 4 quadrants
            q1 = Splitter(b).apply_planar_split(cq.Vector(0,0,0), cq.Vector(1,0,0))
            for q in q1:
                final_cylinder.extend(Splitter(q).apply_planar_split(cq.Vector(0,0,0), cq.Vector(0,1,0)))
    
    res1 = validator.validate_split(model, final_cylinder)
    print(f"🏆 Score: {res1['hex_readiness']['average_score']:.1f} (Bodies: {len(final_cylinder)})")

    # --- 2. LV4 FINAL BOSS (High-Precision Decomposition) ---
    print("\n💎 [Expert] Processing LV4 FINAL BOSS...")
    model2 = cq.importers.importStep(os.path.join(input_dir, "lv4_final_boss.step"))
    # Separate Boss
    boss_parts = Splitter(model2).apply_planar_split(cq.Vector(50,0,0), cq.Vector(1,0,0))
    final_boss = []
    for b in boss_parts:
        if b.val().BoundingBox().center.x > 50: # Boss side
            # Transverse cut at hole center
            parts = Splitter(b).apply_planar_split(cq.Vector(70,0,0), cq.Vector(1,0,0))
            for p in parts:
                # O-Grid on hole
                final_boss.extend(Splitter(p).apply_ogrid(cq.Vector(70,0,0), cq.Vector(0,0,1), radius=15))
        else: # Block side
            # Horizontal cut at blind hole bottom (Z=5 since top is 25 and depth is 20)
            parts = Splitter(b).apply_planar_split(cq.Vector(0,0,5), cq.Vector(0,0,1))
            for p in parts:
                if p.val().BoundingBox().zmax > 20: # Top part with hole
                    final_boss.extend(Splitter(p).apply_ogrid(cq.Vector(0,0,0), cq.Vector(0,0,1), radius=20))
                else: # Clean bottom
                    final_boss.append(p)

    res2 = validator.validate_split(model2, final_boss)
    print(f"🏆 Score: {res2['hex_readiness']['average_score']:.1f} (Bodies: {len(final_boss)})")

if __name__ == "__main__":
    gemini_perfect_split()
