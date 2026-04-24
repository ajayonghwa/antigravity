import cadquery as cq
import time
from .splitter import Splitter
from .classifier import Classifier

class StrategyPlanner:
    def __init__(self, model, max_bodies=20, max_time=10, target_score=90, min_vol_ratio=0.03):
        if not hasattr(model, "val"):
            self.model = cq.Workplane("XY").add(model)
        else:
            self.model = model
        self.classifier = Classifier(self.model)
        self.max_bodies = max_bodies
        self.total_volume = self.model.val().Volume()

    def plan_and_execute(self):
        """Advanced iterative decomposition with priority-based feature slicing."""
        print(f"🚀 Starting Advanced Decomposition...")
        active_bodies = [self.model]
        report = self.classifier.get_feature_report()
        
        # 1. Layering (Step Slicing)
        z_levels = report.get("steps", [])
        for z in z_levels:
            new_bodies = []
            for body in active_bodies:
                bbox = body.val().BoundingBox()
                if bbox.zmin + 0.1 < z < bbox.zmax - 0.1:
                    new_bodies.extend(Splitter(body).apply_planar_split(cq.Vector(0,0,z), cq.Vector(0,0,1)))
                else:
                    new_bodies.append(body)
            active_bodies = new_bodies

        # 2. Feature Slicing with Priority
        # O-GRID (curved slicing) should happen BEFORE Sectoring and others
        def strategy_priority(f):
            s = f.get("strategy")
            if s == "O-GRID": return 0
            if s == "BOUNDARY_ISOLATION": return 1
            if s == "H-GRID": return 2
            return 3
            
        sorted_features = sorted(report["features"], key=strategy_priority)
        
        for feat in sorted_features:
            centers = [cq.Vector(*c) for c in feat.get("centers", [])]
            radius = feat["radius"]
            strategy = feat["strategy"]
            
            for center in centers:
                new_bodies = []
                for body in active_bodies:
                    try:
                        if strategy == "O-GRID":
                            new_bodies.extend(Splitter(body).apply_ogrid_split(center, radius, cq.Vector(0,0,1)))
                        elif strategy == "BOUNDARY_ISOLATION":
                            # Isolation split: Cut in X and Y to isolate the feature from boundary
                            p1 = Splitter(body).apply_planar_split(center, cq.Vector(1,0,0))
                            for b in p1: new_bodies.extend(Splitter(b).apply_planar_split(center, cq.Vector(0,1,0)))
                        elif strategy == "H-GRID":
                            new_bodies.extend(Splitter(body).apply_hgrid_split(center, radius, cq.Vector(0,0,1)))
                        else:
                            new_bodies.append(body)
                    except:
                        new_bodies.append(body)
                if new_bodies: active_bodies = new_bodies
                
        # 3. Sectoring (Global X/Y splits) - Only for non-boxes
        bbox = self.model.val().BoundingBox()
        center = bbox.center
        for normal in [cq.Vector(1,0,0), cq.Vector(0,1,0)]:
            new_bodies = []
            for body in active_bodies:
                if self.classifier.is_primitive(body) != "Box":
                    new_bodies.extend(Splitter(body).apply_planar_split(center, normal))
                else:
                    new_bodies.append(body)
            active_bodies = new_bodies

        return [b for b in active_bodies if b.val().Volume() > self.total_volume * 0.001][:self.max_bodies]
