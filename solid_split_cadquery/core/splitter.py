import cadquery as cq

class Splitter:
    def __init__(self, model):
        self.model = model if isinstance(model, cq.Workplane) else cq.Workplane("XY").add(model)

    def apply_planar_split(self, origin, normal):
        """Standard planar split that always worked."""
        try:
            solid = self.model.val()
            wp = cq.Workplane(cq.Plane(origin=origin, normal=normal))
            cutter = wp.rect(10000, 10000).extrude(10000).val()
            side_a = solid.intersect(cutter)
            side_b = solid.cut(cutter)
            res = []
            if side_a and side_a.Volume() > 1e-6: res.append(cq.Workplane("XY").add(side_a))
            if side_b and side_b.Volume() > 1e-6: res.append(cq.Workplane("XY").add(side_b))
            return res if res else [self.model]
        except:
            return [self.model]

    def apply_hgrid_split(self, center, radius, axis):
        """Extract a rectangular core using 4 planar splits (X+, X-, Y+, Y-)."""
        side = radius * 0.6 # Use 0.6 for a well-sized core
        
        # 1. X-axis splits (Left and Right)
        active = [self.model]
        for offset in [side, -side]:
            next_gen = []
            for body in active:
                next_gen.extend(Splitter(body).apply_planar_split(center + cq.Vector(offset, 0, 0), cq.Vector(1, 0, 0)))
            active = next_gen
            
        # 2. Y-axis splits (Top and Bottom)
        for offset in [side, -side]:
            next_gen = []
            for body in active:
                next_gen.extend(Splitter(body).apply_planar_split(center + cq.Vector(0, offset, 0), cq.Vector(0, 1, 0)))
            active = next_gen
            
        return active
            
    def apply_ogrid_split(self, center, radius, axis):
        """O-Grid: Separate into inner and outer parts using the cylindrical surface as a cutter."""
        # Use exact radius to follow the cylindrical face
        cutter = cq.Workplane(cq.Plane(origin=center, normal=axis)).circle(radius).extrude(10000, both=True).val()
        
        solid = self.model.val()
        try:
            inner = solid.intersect(cutter)
            outer = solid.cut(cutter)
            res = []
            if inner and inner.Volume() > 1e-6: res.append(cq.Workplane("XY").add(inner))
            if outer and outer.Volume() > 1e-6: res.append(cq.Workplane("XY").add(outer))
            return res if res else [self.model]
        except:
            return [self.model]
