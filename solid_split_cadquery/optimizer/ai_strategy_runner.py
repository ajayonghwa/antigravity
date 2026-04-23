import sys
import os
import json
import cadquery as cq

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.splitter import Splitter
from core.classifier import Classifier
from validator.engine import ValidationEngine

class AIStrategyRunner:
    def __init__(self, plans_path=None):
        if plans_path is None:
            plans_path = os.path.join(os.path.dirname(__file__), "ai_plans.json")
        with open(plans_path, "r", encoding="utf-8") as f:
            self.plans = json.load(f)
        self.validator = ValidationEngine()

    def run_all(self):
        print("🚀 Starting AI-Guided Decomposition...")
        results_summary = {}
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        for filename, strategy_list in self.plans.items():
            input_path = os.path.join(project_root, "input", filename)
            if not os.path.exists(input_path):
                print(f"⚠️ Skipping {filename}: File not found.")
                continue

            print(f"Processing {filename}...")
            model = cq.importers.importStep(input_path)
            
            # Start with the full model as a list of bodies
            current_bodies = [model]
            
            for op in strategy_list:
                strategy = op["strategy"]
                params = op.get("params", {})
                print(f" - Applying {strategy}: {op['reasoning']}")
                
                next_bodies = []
                for body in current_bodies:
                    if body.val() is None: continue
                    try:
                        bbox = body.val().BoundingBox()
                    except:
                        continue # Skip void bodies
                    
                    splitter = Splitter(body)
                    classifier = Classifier(body)
                    
                    # Auto-detect defaults if not provided
                    center = cq.Vector(*params.get("center", bbox.center))
                    axis = cq.Vector(*params.get("axis", classifier.get_main_axis()))
                    
                    if strategy == "OGRID":
                        radius = params.get("radius")
                        if radius is None:
                            # Heuristic radius
                            radius = body.val().BoundingBox().xlen * params.get("radius_ratio", 0.3)
                        next_bodies.extend(splitter.apply_ogrid(center, axis, radius))
                        
                    elif strategy == "PLANAR":
                        origin = cq.Vector(*params.get("origin", [0, 0, 0]))
                        normal = cq.Vector(*params.get("normal", [0, 0, 1]))
                        next_bodies.extend(splitter.apply_planar_split(origin, normal))
                        
                    elif strategy == "SECTOR":
                        num_sectors = params.get("num_sectors", 4)
                        next_bodies.extend(splitter.apply_sector_split(center, axis, num_sectors))
                    
                    else:
                        next_bodies.append(body)
                
                current_bodies = next_bodies

            # Validate final result
            val_result = self.validator.validate_split(model, current_bodies)
            results_summary[filename] = {
                "bodies": current_bodies,
                "validation": val_result
            }
            print(f"✅ Finished {filename}. Hex Score: {val_result['hex_readiness']['average_score']:.1f}")

        return results_summary

if __name__ == "__main__":
    runner = AIStrategyRunner()
    summary = runner.run_all()
    # Note: Report generation logic can be integrated here or run separately.
