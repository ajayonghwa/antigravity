import cadquery as cq
import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from loguru import logger

class GeometryExtractor:
    def __init__(self, model):
        self.model = model

    def _get_face_type(self, face):
        adaptor = BRepAdaptor_Surface(face.wrapped)
        stype = adaptor.GetType()
        if stype == GeomAbs_Cylinder: return "Cylinder"
        if stype == GeomAbs_Plane: return "Plane"
        return "Other"

    def _get_cylinder_info(self, face):
        cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
        radius = cyl.Radius()
        loc = cyl.Location()
        axis = cyl.Axis().Direction()
        return {
            "radius": round(radius, 3),
            "location": [round(loc.X(), 3), round(loc.Y(), 3), round(loc.Z(), 3)],
            "axis": [round(axis.X(), 3), round(axis.Y(), 3), round(axis.Z(), 3)]
        }

    def _is_internal_cylinder(self, face):
        try:
            cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
            axis_pos = cq.Vector(cyl.Location().X(), cyl.Location().Y(), cyl.Location().Z())
            axis_dir = cq.Vector(cyl.Axis().Direction().X(), cyl.Axis().Direction().Y(), cyl.Axis().Direction().Z())
            
            pnt = face.positionAt(0.5, 0.5)
            normal = face.normalAt(pnt)
            
            v = pnt - axis_pos
            center_on_axis = axis_pos + axis_dir * v.dot(axis_dir)
            
            radial = (pnt - center_on_axis).normalized()
            return normal.dot(radial) < 0
        except Exception:
            return False

    def detect_cylindrical_features(self):
        """실린더 면들을 분석하고 동축(Coaxial) 그룹으로 묶어 복합 피처를 감지합니다."""
        cyl_faces = []
        for face in self.model.faces().vals():
            if self._get_face_type(face) == "Cylinder":
                info = self._get_cylinder_info(face)
                info["is_internal"] = self._is_internal_cylinder(face)
                cyl_faces.append(info)
        
        # 동축 그룹화 (같은 위치와 방향의 축을 공유하는지 확인)
        coaxial_groups = []
        for info in cyl_faces:
            found = False
            for group in coaxial_groups:
                # 축 방향 일치 확인
                axis_match = np.allclose(group["axis"], info["axis"], atol=1e-3) or \
                             np.allclose(group["axis"], [-a for a in info["axis"]], atol=1e-3)
                # 축 상의 위치 확인 (축 방향 벡터와 두 위치의 차이가 평행한지)
                if axis_match:
                    v = np.array(info["location"]) - np.array(group["location"])
                    if np.linalg.norm(v) < 1e-3: # 시작점 동일
                        dist_to_axis = 0
                    else:
                        v_norm = v / np.linalg.norm(v)
                        dist_to_axis = np.linalg.norm(np.cross(v_norm, group["axis"]))
                    
                    if dist_to_axis < 0.1: # 같은 축 선상에 있음
                        group["elements"].append(info)
                        found = True
                        break
            
            if not found:
                coaxial_groups.append({
                    "axis": info["axis"],
                    "location": info["location"],
                    "elements": [info]
                })
        
        features = []
        for group in coaxial_groups:
            elements = group["elements"]
            if len(elements) > 1:
                # 튜브(Tube) 판별: 동일 위치에 내경/외경이 공존하는 경우
                internals = [e for e in elements if e["is_internal"]]
                externals = [e for e in elements if not e["is_internal"]]
                
                if internals and externals:
                    features.append({
                        "type": "stepped_tube" if len(elements) > 2 else "tube",
                        "axis": group["axis"],
                        "inner_radii": sorted([e["radius"] for e in internals]),
                        "outer_radii": sorted([e["radius"] for e in externals]),
                        "location": group["location"]
                    })
                else:
                    # 단차가 있는 형상 (Stepped Hole or Stepped Shaft)
                    is_mostly_internal = len(internals) > len(externals)
                    features.append({
                        "type": "stepped_hole" if is_mostly_internal else "stepped_shaft",
                        "axis": group["axis"],
                        "radii": sorted([e["radius"] for e in elements]),
                        "element_count": len(elements),
                        "location": group["location"]
                    })
            else:
                # 단일 실린더/구멍
                e = elements[0]
                features.append({
                    "type": "hole" if e["is_internal"] else "cylinder",
                    "radius": e["radius"],
                    "location": e["location"],
                    "axis": e["axis"]
                })
        return features

    def _is_concave_edge(self, edge, faces):
        """에지가 오목(Concave)한지 판별합니다. 오목한 에지는 형상 결합의 강력한 신호입니다."""
        try:
            adj_faces = []
            for f in faces:
                if any(e.isSame(edge) for e in f.Edges()):
                    adj_faces.append(f)
            
            if len(adj_faces) != 2: 
                return False
            
            pnt = edge.positionAt(0.5)
            n1 = adj_faces[0].normalAt(pnt)
            
            c1 = adj_faces[0].Center()
            c2 = adj_faces[1].Center()
            v_between = (c2 - c1).normalized()
            
            dot_val = n1.dot(v_between)
            return dot_val > 0.1
        except Exception:
            return False

    def detect_junctions(self):
        """형상 간의 이음매(오목한 경계)를 감지하여 분할 후보 지점을 추출합니다."""
        junctions = []
        all_faces = self.model.solids().faces().vals()
        all_edges = self.model.solids().edges().vals()
        
        for edge in all_edges:
            if self._is_concave_edge(edge, all_faces):
                pnt = edge.positionAt(0.5)
                # 인접 면 타입 파악
                adj_faces = [f for f in all_faces if any(e.isSame(edge) for e in f.Edges())]
                types = sorted([self._get_face_type(f) for f in adj_faces])
                
                junctions.append({
                    "type": "junction",
                    "location": [round(pnt.x, 3), round(pnt.y, 3), round(pnt.z, 3)],
                    "connection": f"{types[0]}-{types[1]}",
                    "reason": "Concave boundary"
                })
        
        # 근접한 정션 포인트 그룹화 (중복 제거)
        unique_junctions = []
        for j in junctions:
            exists = False
            for uj in unique_junctions:
                dist = np.linalg.norm(np.array(j["location"]) - np.array(uj["location"]))
                if dist < 2.0: # 2mm 이내 그룹화
                    exists = True
                    break
            if not exists:
                unique_junctions.append(j)
                
        return unique_junctions

    def detect_steps(self):
        z_levels = []
        for face in self.model.faces().vals():
            if self._get_face_type(face) == "Plane":
                n = face.normalAt(face.Center())
                if abs(n.z) > 0.99:
                    z_levels.append(round(face.Center().z, 3))
        
        if not z_levels: return []
        z_levels = sorted(list(set(z_levels)))
        
        # Merge close levels
        merged = [z_levels[0]]
        for z in z_levels[1:]:
            if z - merged[-1] > 0.1:
                merged.append(z)
        
        steps = []
        for i in range(len(merged) - 1):
            steps.append({
                "type": "step",
                "height": round(merged[i+1] - merged[i], 3),
                "location_z": merged[i+1]
            })
        return steps

    def extract_summary(self):
        bbox = self.model.val().BoundingBox()
        summary = {
            "overall_size": [round(bbox.xlen, 3), round(bbox.ylen, 3), round(bbox.zlen, 3)],
            "features": [],
            "mesh_goal": "High-quality Hexahedral mesh for stress analysis"
        }
        
        summary["features"].extend(self.detect_cylindrical_features())
        summary["features"].extend(self.detect_steps())
        summary["features"].extend(self.detect_junctions())
        
        return summary

if __name__ == "__main__":
    # Test with a clear concave edge: Box with a step cut
    model = cq.Workplane("XY").box(20, 20, 20).faces(">Z").workplane(offset=-10).rect(10, 10).cutBlind(-10)
    
    extractor = GeometryExtractor(model)
    import json
    print(json.dumps(extractor.extract_summary(), indent=2))
