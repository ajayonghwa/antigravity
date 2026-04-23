import os
import cadquery as cq
from core.strategy_planner import StrategyPlanner
from validator.engine import ValidationEngine

import json

def run_intelligent_pipeline():
    input_dir = "input"
    output_dir = "output"
    log_path = "progress_log.json"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load existing progress
    progress = {}
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            progress = json.load(f)

    validator = ValidationEngine()
    files = sorted([f for f in os.listdir(input_dir) if f.endswith(".step")])
    print(f"🚀 Running Intelligent Pipeline on {len(files)} files...")

    for filename in files:
        if filename in progress and progress[filename].get("status") == "DONE":
            print(f"⏩ Skipping {filename} (Already done)")
            continue

        print(f"\nProcessing {filename}...")
        try:
            model_path = os.path.join(input_dir, filename)
            model = cq.importers.importStep(model_path)
            
            planner = StrategyPlanner(model)
            split_bodies = planner.plan_and_execute()
            
            base_name = os.path.splitext(filename)[0]
            for i, body in enumerate(split_bodies):
                out_path = os.path.join(output_dir, f"{base_name}_part_{i}.step")
                cq.exporters.export(body, out_path)
                
            val_result = validator.validate_split(model, split_bodies)
            score = val_result['hex_readiness']['average_score']
            print(f"✅ Finished {filename}. Hex Score: {score:.1f}")
            
            # Save progress incrementally
            progress[filename] = {
                "status": "DONE",
                "score": score,
                "bodies": len(split_bodies)
            }
            with open(log_path, "w") as f:
                json.dump(progress, f, indent=4)
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    run_intelligent_pipeline()
