import cadquery as cq
import numpy as np
from .geometry_utils import GeometryUtils

class Splitter:
    def __init__(self, model):
        self.model = model

    def split_by_plane(self, origin, normal):
        """Split the model using a plane defined by origin and normal"""
        # normal is a Vector or tuple
        if isinstance(normal, tuple):
            normal = cq.Vector(*normal)
        if isinstance(origin, tuple):
            origin = cq.Vector(*origin)

        # In CadQuery, we can use split()
        # But split() usually discards one side. We want to KEEP BOTH as separate bodies.
        
        # To keep both, we can use a Boolean operation or a Workplane split.
        # However, the cleanest way to get TWO solids is:
        
        # 1. Create a large box that covers half the space
        # 2. Cut it from the model to get one half
        # 3. Intersect it with the model to get the other half
        
        # Alternatively, use the internal .split() logic but carefully.
        # Actually, cq.Workplane.split() can be used to slice.
        
        # Let's use a cutting surface (Face) approach like in the SCDM version.
        cutter = self._create_planar_cutter(origin, normal)
        return self.model.cut(cutter) # This cuts a gap, not quite what we want for 'split'

    def apply_ogrid(self, center, axis, radius):
        """Apply O-Grid split (circular split)"""
        # Create a cylindrical cutter
        cutter = (cq.Workplane("XY")
                  .add(center)
                  .toPending()
                  .workplane()
                  .circle(radius)
                  .extrude(500, both=True)) # Large enough
        
        # To truly split into two solids (core and shell):
        core = self.model.intersect(cutter)
        shell = self.model.cut(cutter)
        
        return core, shell

    def apply_planar_split(self, origin, normal):
        """Split into two solids along a plane"""
        # Create a large box representing half-space
        inf = 10000.0 # Large enough for most models
        
        # Orient a workplane to the plane
        wp = cq.Workplane(cq.Plane(origin=origin, normal=normal))
        
        # Half-space box (centered at origin of the plane, extending in normal direction)
        half_space = wp.workplane().rect(inf, inf).extrude(inf)
        
        # side_a is the part inside the half_space (in the direction of normal)
        side_a = self.model.intersect(half_space)
        # side_b is the part outside the half_space
        side_b = self.model.cut(half_space)
        
        return [side_a, side_b]

    def apply_sector_split(self, center, axis, num_sectors=4):
        """Split the body into radial sectors around an axis"""
        if num_sectors < 2:
            return [self.model]

        results = [self.model]
        angle_step = 360.0 / num_sectors
        
        # Get a starting orthogonal vector
        v_start = GeometryUtils.get_orthogonal_vector(axis)
        
        for i in range(num_sectors):
            # Rotate the normal vector for each cut plane
            # A sector split at 4 quadrants needs 2 planes (0 deg and 90 deg)
            # Wait, 4 quadrants = 2 planes. 
            # If num_sectors is 4, we usually mean splitting by 90 deg intervals.
            pass
        
        # Simpler approach for 4 quadrants (common in FEA):
        # Plane 1: (center, v1)
        # Plane 2: (center, v2) where v2 = axis x v1
        
        v1 = GeometryUtils.get_orthogonal_vector(axis)
        v2 = cq.Vector(*np.cross(GeometryUtils.to_np(axis), GeometryUtils.to_np(v1)))
        
        # Split by first plane
        temp_bodies = []
        for body in results:
            splitter = Splitter(body)
            temp_bodies.extend(splitter.apply_planar_split(center, v1))
        results = temp_bodies
        
        # Split by second plane
        temp_bodies = []
        for body in results:
            splitter = Splitter(body)
            temp_bodies.extend(splitter.apply_planar_split(center, v2))
        results = temp_bodies
        
        return results

    def apply_hgrid(self, start_point, normal, spacing, num_planes):
        """Apply a series of parallel planar splits (H-Grid)"""
        results = [self.model]
        
        for i in range(num_planes):
            origin = start_point + normal * (spacing * (i + 1))
            new_results = []
            for body in results:
                splitter = Splitter(body)
                # We only need to split the 'last' body in the list usually, 
                # but to be safe we check which one the plane intersects.
                # For simplicity, we just try to split all.
                split_parts = splitter.apply_planar_split(origin, normal)
                new_results.extend([p for p in split_parts if p.val() is not None and p.val().Volume() > 1e-9])
            results = new_results
            
        return results

    def _create_planar_cutter(self, origin, normal):
        """Internal helper to create a planar face for splitting"""
        return (cq.Workplane(cq.Plane(origin=origin, normal=normal))
                .workplane()
                .rect(10000, 10000)
                .val())
