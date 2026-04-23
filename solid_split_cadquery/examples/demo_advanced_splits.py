import sys
import os
import cadquery as cq

# Add core to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.splitter import Splitter
from core.classifier import Classifier

def run_advanced_demo():
    print("🚀 Running Advanced Split Demo (Sector & H-Grid)...")
    
    # 1. Create a base block with a hole
    print(" - Generating test geometry...")
    model = (cq.Workplane("XY").box(100, 100, 100)
             .faces(">Z").workplane().circle(30).cutThruAll())
    
    # 2. Initialize Splitter & Classifier
    splitter = Splitter(model)
    classifier = Classifier(model)
    
    main_axis = classifier.get_main_axis()
    center = model.val().BoundingBox().center
    print(f" - Detected Main Axis: {main_axis}")
    print(f" - Model Center: {center}")
    
    # 3. Apply Sector Split (4 quadrants)
    print(" - Applying Sector Split (4 segments)...")
    sector_bodies = splitter.apply_sector_split(center, main_axis, num_sectors=4)
    print(f"   ㄴ Created {len(sector_bodies)} sector segments.")
    
    # 4. Apply H-Grid (Planar slicing) to one of the sectors
    print(" - Applying H-Grid (slicing) to one segment...")
    target_body = sector_bodies[0]
    hgrid_splitter = Splitter(target_body)
    hgrid_bodies = hgrid_splitter.apply_hgrid(
        start_point=cq.Vector(0, 0, -50),
        normal=main_axis,
        spacing=25,
        num_planes=3
    )
    print(f"   ㄴ Sliced into {len(hgrid_bodies)} pieces.")
    
    # 5. Export results
    output_dir = "output/advanced"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for i, b in enumerate(sector_bodies):
        cq.exporters.export(b, os.path.join(output_dir, f"sector_{i}.step"))
    
    for i, b in enumerate(hgrid_bodies):
        cq.exporters.export(b, os.path.join(output_dir, f"hgrid_piece_{i}.step"))
    
    print(f"✅ Advanced demo finished. Check {output_dir}/ for results.")

if __name__ == "__main__":
    run_advanced_demo()
