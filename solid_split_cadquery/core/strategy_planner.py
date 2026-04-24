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
        """Simple iterative decomposition loop that forced to split."""
        print(f"🚀 Starting Iterative Decomposition...")
        active_bodies = [self.model]
        
        # 1. Macro Analysis
        report = self.classifier.get_feature_report()
        
        # 2. Layering (Step Slicing)
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

        # 3. Feature Slicing (H/O-Grid)
        for feat in report["features"]:
            centers = [cq.Vector(*c) for c in feat.get("centers", [])]
            radius = feat["radius"]
            strategy = feat["strategy"]
            
            for center in centers:
                new_bodies = []
                for body in active_bodies:
                    # 프리미티브 체크 생략 - 무조건 절단 시도
                    try:
                        if strategy == "O-GRID":
                            new_bodies.extend(Splitter(body).apply_ogrid_split(center, radius, cq.Vector(0,0,1)))
                        elif strategy == "H-GRID":
                            new_bodies.extend(Splitter(body).apply_hgrid_split(center, radius, cq.Vector(0,0,1)))
                        else:
                            new_bodies.append(body)
                    except:
                        new_bodies.append(body)
                active_bodies = new_bodies
                
        # 4. Sectoring (Global X/Y splits)
        bbox = self.model.val().BoundingBox()
        center = bbox.center
        for normal in [cq.Vector(1,0,0), cq.Vector(0,1,0)]:
            new_bodies = []
            for body in active_bodies:
                # 무조건 섹터 분할 시도
                try:
                    parts = Splitter(body).apply_planar_split(center, normal)
                    new_bodies.extend(parts)
                except:
                    new_bodies.append(body)
            active_bodies = new_bodies

        # Final Filter
        return [b for b in active_bodies if b.val().Volume() > self.total_volume * 0.001][:self.max_bodies]
