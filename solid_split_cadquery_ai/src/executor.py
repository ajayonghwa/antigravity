import cadquery as cq
from loguru import logger

class SplitExecutor:
    def __init__(self, initial_model):
        # We work with a list of solids. Initially, just one.
        self.solids = initial_model.solids().vals()

    def execute_plan(self, plan, max_parts=50, min_volume_ratio=0.01):
        """
        AI 계획을 실행하여 솔리드를 분할합니다.
        :param max_parts: 허용되는 최대 조각 수
        :param min_volume_ratio: 원래 부피 대비 최소 허용 부피 비율 (예: 0.01 = 1%)
        """
        logger.info(f"Executing plan: {plan.get('strategy_description', 'No description')}")
        
        # 전체 원본 부피 계산
        original_total_volume = sum(s.Volume() for s in self.solids)
        
        for split in plan.get("splits", []):
            if len(self.solids) >= max_parts:
                logger.warning(f"Reached max parts limit ({max_parts}). Stopping further splits.")
                break
                
            op = split.get("operation")
            if op == "plane_cut":
                self._plane_cut(split)
            elif op == "hole_isolation":
                self._hole_isolation(split)
            else:
                logger.warning(f"Unknown operation: {op}")

            # 분할 후 부피 유효성 체크
            for s in self.solids:
                if s.Volume() < original_total_volume * min_volume_ratio:
                    logger.warning(f"Extremely small part detected ({s.Volume():.2f}). Consider adjusting strategy.")
        
        return self.solids

    def _plane_cut(self, split):
        axis = split.get("axis", "Z").upper()
        coord = split.get("coordinate", 0)
        reason = split.get("reason", "")
        
        logger.info(f"Performing plane cut: axis={axis}, coord={coord} ({reason})")
        
        new_solids = []
        for solid in self.solids:
            try:
                # Create a cutter plane
                if axis == "X":
                    cutter = cq.Workplane("YZ").workplane(offset=coord).rect(1000, 1000).extrude(0.1, both=True)
                elif axis == "Y":
                    cutter = cq.Workplane("XZ").workplane(offset=coord).rect(1000, 1000).extrude(0.1, both=True)
                else: # Z
                    cutter = cq.Workplane("XY").workplane(offset=coord).rect(1000, 1000).extrude(0.1, both=True)
                
                # Use split() if possible, or boolean cut
                # CadQuery's split() can be tricky. A common robust way is to use a large box or plane.
                # Here we'll use a simple planar split.
                
                # Workplane based split:
                wp = cq.Workplane(solid)
                if axis == "X":
                    result = wp.split(keepTop=True, keepBottom=True)
                elif axis == "Y":
                    # For Y and X, we might need to rotate the workplane
                    # Actually, we can just define the plane
                    plane = cq.Plane(origin=(coord, 0, 0), normal=(1, 0, 0))
                    result = wp.split(keepTop=True, keepBottom=True) # This uses the current WP plane
                
                # To be robust, let's use a more direct approach:
                # We'll use the .split() method on Workplane which uses the current plane.
                
                if axis == "Z":
                    res = cq.Workplane(solid).workplane(offset=coord).split(keepTop=True, keepBottom=True)
                elif axis == "X":
                    res = cq.Workplane(solid).transformed(rotate=(0, 90, 0), offset=(0, 0, coord)).split(keepTop=True, keepBottom=True)
                elif axis == "Y":
                    res = cq.Workplane(solid).transformed(rotate=(90, 0, 0), offset=(0, 0, coord)).split(keepTop=True, keepBottom=True)
                else:
                    res = cq.Workplane(solid) # No change
                
                new_solids.extend(res.solids().vals())
            except Exception as e:
                logger.error(f"Plane cut failed: {e}")
                new_solids.append(solid)
        
        self.solids = new_solids

    def _hole_isolation(self, split):
        feature_index = split.get("feature_index", 0)
        method = split.get("method", "butterfly")
        reason = split.get("reason", "")
        
        logger.info(f"Performing hole isolation: index={feature_index}, method={method} ({reason})")
        
        # We need the summary info to find the hole. 
        # For simplicity in this implementation, we'll assume the feature_index 
        # refers to the hole patterns detected by the extractor.
        # However, to be robust, the AI should provide coordinates.
        # Let's assume the AI provides 'center' and 'radius' in the split command if it can.
        
        center = split.get("center")
        radius = split.get("radius")
        
        if not center or not radius:
            logger.warning("Hole isolation skipped: missing center or radius in command.")
            return

        # Simple isolation: cut at x +/- R*1.5 and y +/- R*1.5
        margin = 1.5
        cx, cy, cz = center
        offsets_x = [cx - radius * margin, cx + radius * margin]
        offsets_y = [cy - radius * margin, cy + radius * margin]

        for ox in offsets_x:
            self._plane_cut({"axis": "X", "coordinate": ox, "reason": f"Hole isolation X {ox}"})
        for oy in offsets_y:
            self._plane_cut({"axis": "Y", "coordinate": oy, "reason": f"Hole isolation Y {oy}"})

    def save_results(self, output_dir):
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i, solid in enumerate(self.solids):
            path = os.path.join(output_dir, f"split_{i:03d}.step")
            cq.exporters.export(cq.Workplane(solid), path)
        logger.info(f"Saved {len(self.solids)} solids to {output_dir}")
