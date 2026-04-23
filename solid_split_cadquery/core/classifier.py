import cadquery as cq
import numpy as np
from .geometry_utils import GeometryUtils

class Classifier:
    def __init__(self, model):
        self.model = model

    def classify_faces(self):
        """Classify all faces in the model into features"""
        results = []
        faces = self.model.faces().vals()
        
        for i, face in enumerate(faces):
            f_type = self._get_face_type(face)
            center = face.Center()
            
            feature = {
                "id": i,
                "type": f_type,
                "center": center,
                "area": face.Area(),
                "is_internal": False
            }
            
            if f_type == "Cylinder":
                feature["is_internal"] = self._is_internal_cylinder(face)
                feature["radius"] = self._get_cylinder_radius(face)
                
            results.append(feature)
        return results

    def _get_cylindrical_faces(self):
        """Get all cylindrical faces in the model"""
        return [f for f in self.model.faces().vals() if self._get_face_type(f) == "Cylinder"]

    def get_main_axis(self):
        """Determine the main axis of the model based on cylindrical faces"""
        cyl_faces = [f for f in self.model.faces().vals() if self._get_face_type(f) == "Cylinder"]
        if not cyl_faces:
            # Fallback to longest dimension of bbox
            bbox = self.model.val().BoundingBox()
            dims = [bbox.xlen, bbox.ylen, bbox.zlen]
            max_dim = np.argmax(dims)
            axis = [0, 0, 0]
            axis[max_dim] = 1
            return cq.Vector(*axis)
            
        axes = []
        for f in cyl_faces:
            try:
                # OCCT can give the axis of the surface
                axis = f.wrapped.Surface().Value().Cylinder().Axis().Direction()
                axes.append(cq.Vector(axis.X(), axis.Y(), axis.Z()))
            except:
                pass
        
        if not axes:
            return cq.Vector(0, 0, 1)
            
        # Group similar axes
        unique_axes = []
        for a in axes:
            # Normalize and handle sign ambiguity
            a_np = GeometryUtils.to_np(a)
            if a_np[0] < 0 or (a_np[0] == 0 and a_np[1] < 0) or (a_np[0] == 0 and a_np[1] == 0 and a_np[2] < 0):
                a_np = -a_np
            
            matched = False
            for ua in unique_axes:
                if np.linalg.norm(ua - a_np) < 0.05:
                    matched = True
                    break
            if not matched:
                unique_axes.append(a_np)
        
        # For now, return the most common axis (simplified)
        return cq.Vector(*unique_axes[0])

    def _get_face_type(self, face):
        """Identify face type (Cylinder, Plane, etc.) using OCCT Adaptor"""
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Sphere
        
        adaptor = BRepAdaptor_Surface(face.wrapped)
        surf_type = adaptor.GetType()
        
        if surf_type == GeomAbs_Cylinder:
            return "Cylinder"
        elif surf_type == GeomAbs_Plane:
            return "Plane"
        elif surf_type == GeomAbs_Sphere:
            return "Sphere"
        else:
            return "Other"

    def _is_internal_cylinder(self, face):
        """Check if cylindrical face points inward (hole) or outward (boss)"""
        try:
            from OCP.BRepAdaptor import BRepAdaptor_Surface
            adaptor = BRepAdaptor_Surface(face.wrapped)
            cylinder = adaptor.Cylinder()
            center = cq.Vector(cylinder.Location())
            
            # Sample a point on face and its normal
            pnt = face.Center()
            normal = face.normalAt(pnt)
            
            # Vector from center to point
            radial = (pnt - center).normalized()
            dot = normal.dot(radial)
            
            # If normal points opposite to radial vector, it's a hole (internal)
            return dot < 0
        except:
            return False

    def _get_cylinder_radius(self, face):
        """Get radius of a cylindrical face"""
        try:
            from OCP.BRepAdaptor import BRepAdaptor_Surface
            return BRepAdaptor_Surface(face.wrapped).Cylinder().Radius()
        except:
            bbox = face.BoundingBox()
            return (bbox.xlen + bbox.ylen) / 4

    def get_whr_for_hole(self, hole_face):
        """
        Calculate Wall-to-Hole Ratio (WHR) for a given cylindrical face.
        WHR = Distance to nearest outer wall / Hole Radius
        """
        import numpy as np
        from cadquery import Vector
        
        # 1. Get hole properties
        try:
            from OCP.BRepAdaptor import BRepAdaptor_Surface
            adaptor = BRepAdaptor_Surface(hole_face.wrapped)
            cylinder = adaptor.Cylinder()
            radius = cylinder.Radius()
            center = cq.Vector(cylinder.Location())
        except:
            return 999.0 # Not a cylinder or error
            
        # 2. Find distance to the nearest outer face (that is not this hole)
        min_dist = float('inf')
        all_faces = self.model.faces().vals()
        
        for face in all_faces:
            if face.hashCode() == hole_face.hashCode():
                continue
            
            # Simple distance from center to face
            dist = face.distance(cq.Vertex.makeVertex(*center.toTuple()))
            if dist < min_dist:
                min_dist = dist
        
        whr = min_dist / radius if radius > 0 else 999.0
        return whr

    def get_feature_report(self):
        """
        Generate a comprehensive report of all features including WHR.
        """
        report = {"holes": [], "main_axis": self.get_main_axis().toTuple()}
        cylinders = self._get_cylindrical_faces()
        
        for cyl in cylinders:
            is_internal = self._is_internal_cylinder(cyl)
            whr = self.get_whr_for_hole(cyl)
            
            report["holes"].append({
                "center": cyl.Center().toTuple(),
                "radius": self._get_cylinder_radius(cyl),
                "is_internal": is_internal,
                "whr": whr,
                "action_recommended": "OGRID" if 1.0 <= whr <= 6.0 else "SKIP_OGRID"
            })
            
        return report
