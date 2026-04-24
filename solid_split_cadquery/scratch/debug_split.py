import cadquery as cq
from core.strategy_planner import StrategyPlanner
from core.classifier import Classifier

model_path = "examples/models/auto_stepped.step"
model = cq.importers.importStep(model_path)
planner = StrategyPlanner(model)

print(f"Initial volume: {model.val().Volume()}")
report = planner.classifier.get_feature_report()
print(f"Detected steps: {report['steps']}")

# Manual Step Slice test
z = report['steps'][0]
from core.splitter import Splitter
parts = Splitter(model).apply_planar_split(cq.Vector(0,0,z), cq.Vector(0,0,1))
print(f"Planar split at Z={z} produced {len(parts)} parts")
for i, p in enumerate(parts):
    print(f"  Part {i} volume: {p.val().Volume()}")
