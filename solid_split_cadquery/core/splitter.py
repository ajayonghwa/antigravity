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
        side = radius * 0.5 * 2.0
        cutter = cq.Workplane(cq.Plane(origin=center, normal=axis)).box(side, side, 10000).val()
        solid = self.model.val()
        try:
            core = solid.intersect(cutter)
            shell = solid.cut(cutter)
            res = []
            if core and core.Volume() > 1e-6: res.append(cq.Workplane("XY").add(core))
            if shell and shell.Volume() > 1e-6: res.append(cq.Workplane("XY").add(shell))
            return res if res else [self.model]
        except:
            return [self.model]
            
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
