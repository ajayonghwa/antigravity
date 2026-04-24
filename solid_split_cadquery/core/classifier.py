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
                    z_levels.append(face.Center().z)
        if not z_levels: return []
        z_levels = sorted(list(set(z_levels)))
        
        # 0.5mm 이내의 단차는 하나로 병합
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
        
        cyl_features = []
        for f in self.model.faces().vals():
            if self._get_face_type(f) == "Cylinder":
                radius = self._get_cylinder_radius(f)
                if radius < 0.5: continue
                
                cyl_geom = BRepAdaptor_Surface(f.wrapped).Cylinder()
                loc = cyl_geom.Location()
                actual_center = (loc.X(), loc.Y(), loc.Z())
                is_internal = self._is_internal_cylinder(f)
                
                # 중복 제거: 0.5mm 이내의 거리와 동일 반지름은 하나로 취급
                exists = False
                for feat in cyl_features:
                    old_c = feat["centers"][0]
                    dist = ((old_c[0]-actual_center[0])**2 + (old_c[1]-actual_center[1])**2)**0.5
                    if abs(feat["radius"] - radius) < 0.1 and dist < 0.5:
                        exists = True
                        break
                
                    is_main_disk = radius > min(bbox.xlen, bbox.ylen) * 0.3
                    
                    # 전략 결정 로직 세분화
                    if is_main_disk:
                        strategy = "O-GRID"
                    elif is_internal:
                        # 내부 구멍이고 외벽과 충분히 멀면 H-GRID (격자 품질 우선)
                        # 적당히 가까우면 BOUNDARY_ISOLATION, 아주 가까우면 O-GRID
                        if min_dist > radius * 4.0:
                            strategy = "H-GRID"
                        elif min_dist > radius * 2.5:
                            strategy = "BOUNDARY_ISOLATION"
                        else:
                            strategy = "O-GRID"
                    else:
                        # 돌출부(Boss)는 사용자 요청에 따라 옆면 절단(O-GRID) 수행
                        strategy = "O-GRID"
                    
                    cyl_features.append({
                        "type": "hole" if is_internal else "cylinder",
                        "radius": radius,
                        "centers": [actual_center],
                        "strategy": strategy
                    })
        
        report["features"].extend(cyl_features)
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
