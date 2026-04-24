import os
import cadquery as cq
from src.extractor import GeometryExtractor
from src.planner import AIPlanner
from src.executor import SplitExecutor
from loguru import logger

def create_sample_geometry():
    logger.info("Creating sample geometry for demonstration...")
    # Plate with 4 holes and a step
    plate = cq.Workplane("XY").box(100, 100, 10)
    for loc in [(25, 25), (25, 75), (75, 25), (75, 75)]:
        plate = plate.faces(">Z").workplane().move(*loc).hole(5)
    plate = plate.faces(">Z").workplane().rect(50, 50).extrude(5)
    return plate

def main():
    input_dir = "data/input"
    output_dir = "data/output"
    
    # 1. Load Geometry
    step_files = [f for f in os.listdir(input_dir) if f.endswith(".step")]
    
    if not step_files:
        logger.warning("No STEP files found in data/input. Using sample geometry.")
        model = create_sample_geometry()
        model_name = "sample_plate"
    else:
        model_path = os.path.join(input_dir, step_files[0])
        logger.info(f"Loading model: {model_path}")
        model = cq.importers.importStep(model_path)
        model_name = os.path.splitext(step_files[0])[0]

    # 2. Extract Geometric Info
    logger.info("Extracting geometric features...")
    extractor = GeometryExtractor(model)
    summary = extractor.extract_summary()
    logger.info(f"Summary: {summary}")

    # 3. Get AI Plan
    logger.info("Getting splitting plan from AI...")
    planner = AIPlanner()
    plan = planner.plan_splits(summary)
    logger.info(f"Plan: {plan}")

    # 4. Execute Splits
    logger.info("Executing splitting operations...")
    executor = SplitExecutor(model)
    results = executor.execute_plan(plan)
    
    # 5. Save Output
    final_output_dir = os.path.join(output_dir, model_name)
    executor.save_results(final_output_dir)
    logger.info("Decomposition complete.")

if __name__ == "__main__":
    main()
