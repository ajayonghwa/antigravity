import cadquery as cq
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

class Classifier:
    def __init__(self, model):
        self.model = model

    def _get_face_type(self, face):
        adaptor = BRepAdaptor_Surface(face.wrapped)
        stype = adaptor.GetType()
        if stype == GeomAbs_Cylinder: return "Cylinder"
        if stype == GeomAbs_Plane: return "Plane"
        return "Other"

    def _get_cylinder_radius(self, face):
        return BRepAdaptor_Surface(face.wrapped).Cylinder().Radius()

    def _is_internal_cylinder(self, face):
        try:
            cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
            center = cq.Vector(cyl.Location().X(), cyl.Location().Y(), cyl.Location().Z())
            pnt = face.Center()
            normal = face.normalAt(pnt)
            radial = (pnt - center).normalized()
            return normal.dot(radial) < 0
        except: return False

    def detect_steps(self):
        z_levels = []
        for face in self.model.faces().vals():
            if self._get_face_type(face) == "Plane":
                n = face.normalAt(face.Center())
                if abs(n.z) > 0.99:
                    z_levels.append(round(face.Center().z, 3))
        if not z_levels: return []
        z_levels = sorted(list(set(z_levels)))
        unique = [z_levels[0]]
        for z in z_levels[1:]:
            if z - unique[-1] > 0.5: unique.append(z)
        return unique

    def get_feature_report(self):
        bbox = self.model.val().BoundingBox()
        report = {
            "overall_size": (bbox.xlen, bbox.ylen, bbox.zlen),
            "features": [],
            "steps": self.detect_steps(),
            "main_axis": (0,0,1)
        }
        
        for f in self.model.faces().vals():
            if self._get_face_type(f) == "Cylinder":
                radius = self._get_cylinder_radius(f)
                if radius < 0.5: continue
                
                center = f.Center()
                is_internal = self._is_internal_cylinder(f)
                
                dist_to_walls = [abs(center.x - bbox.xmin), abs(center.x - bbox.xmax), abs(center.y - bbox.ymin), abs(center.y - bbox.ymax)]
                
                feat = {
                    "type": "hole" if is_internal else "cylinder",
                    "radius": radius,
                    "centers": [center.toTuple()],
                    "strategy": "BOUNDARY_ISOLATION" if min(dist_to_walls) < radius * 2.5 else ("O-GRID" if is_internal else "H-GRID")
                }
                report["features"].append(feat)
        return report

    def is_primitive(self, body):
        try:
            faces = body.faces().vals()
            face_count = len(faces)
            types = [self._get_face_type(f) for f in faces]
            if face_count == 6 and all(t == "Plane" for t in types): return "Box"
            if face_count == 3 and types.count("Cylinder") == 1: return "Full_Cylinder"
            if face_count == 4 and types.count("Cylinder") == 2: return "Hollow_Cylinder"
        except: pass
        return None
