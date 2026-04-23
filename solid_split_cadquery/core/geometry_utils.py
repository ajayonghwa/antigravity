import numpy as np
from cadquery import Vector

class GeometryUtils:
    @staticmethod
    def to_np(vector):
        """Convert CadQuery Vector to numpy array"""
        return np.array([vector.x, vector.y, vector.z])

    @staticmethod
    def normalize(v):
        """Normalize a vector"""
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    @staticmethod
    def get_bbox_center(obj):
        """Get the center of the bounding box of a CadQuery object"""
        if hasattr(obj, "val"):
            bbox = obj.val().BoundingBox()
        else:
            bbox = obj.BoundingBox()
        return Vector(
            (bbox.xmin + bbox.xmax) / 2,
            (bbox.ymin + bbox.ymax) / 2,
            (bbox.zmin + bbox.zmax) / 2
        )

    @staticmethod
    def get_orthogonal_vector(v):
        """Find a vector orthogonal to the given vector v"""
        v_np = GeometryUtils.to_np(v)
        if abs(v_np[0]) < 0.9:
            ref = np.array([1, 0, 0])
        else:
            ref = np.array([0, 1, 0])
        
        ortho = np.cross(v_np, ref)
        return Vector(*GeometryUtils.normalize(ortho))
