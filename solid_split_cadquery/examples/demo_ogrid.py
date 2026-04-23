import sys
import os
import cadquery as cq

# Add core to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.splitter import Splitter

def run_demo():
    print("🚀 Running O-Grid Split Demo...")
    
    # 1. Create a simple cylinder
    cylinder = cq.Workplane("XY").circle(50).extrude(100)
    
    # 2. Initialize Splitter
    splitter = Splitter(cylinder)
    
    # 3. Apply O-Grid (Core radius 30)
    print(" - Applying O-Grid split (radius=30)...")
    core, shell = splitter.apply_ogrid(cq.Vector(0,0,0), cq.Vector(0,0,1), 30)
    
    # 4. Export results
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    cq.exporters.export(core, os.path.join(output_dir, "demo_ogrid_core.step"))
    cq.exporters.export(shell, os.path.join(output_dir, "demo_ogrid_shell.step"))
    
    print(f"✅ Demo finished. Check {output_dir}/ for results:")
    print("   - demo_ogrid_core.step")
    print("   - demo_ogrid_shell.step")

if __name__ == "__main__":
    run_demo()
