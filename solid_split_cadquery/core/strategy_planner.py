import cadquery as cq
import os
import numpy as np
import time
from .splitter import Splitter
from .classifier import Classifier
from validator.engine import ValidationEngine

class StrategyPlanner:
    def __init__(self, model, max_bodies=40, max_time=15, target_score=85, min_vol_ratio=0.02):
        # [Expert] Keep the Workplane fix for stability
        if not hasattr(model, "val"):
            self.model = cq.Workplane("XY").add(model)
        else:
            self.model = model
        self.classifier = Classifier(model)
        self.global_report = self.classifier.get_feature_report()
        self.main_axis = cq.Vector(*self.global_report["main_axis"])
        self.validator = ValidationEngine()
        
        # User Configuration
        self.max_bodies = max_bodies
        self.max_time = max_time
        self.target_score = target_score
        self.min_vol_ratio = min_vol_ratio
        
        self.start_time = time.time()
        self.total_volume = self.model.val().Volume()
        self.snap_eps = 1.0 # Reverted to 1.0mm

    def _get_local_features(self, body):
        bbox = body.val().BoundingBox()
        local_holes = []
        for hole in self.global_report["holes"]:
            c = cq.Vector(*hole["center"])
            if (bbox.xmin - 0.1 <= c.x <= bbox.xmax + 0.1 and 
                bbox.ymin - 0.1 <= c.y <= bbox.ymax + 0.1 and 
                bbox.zmin - 0.1 <= c.z <= bbox.zmax + 0.1):
                local_holes.append(hole)
        return local_holes

    def _generate_candidates(self, body, local_holes):
        candidates = []
        bbox = body.val().BoundingBox()
        eps = 2.0 
        
        global_center = cq.Vector(*self.global_report.get("center", [0,0,0]))
        for normal in [cq.Vector(1,0,0), cq.Vector(0,1,0), cq.Vector(0,0,1)]:
            if abs(normal.x) > 0.9 and bbox.xmin + eps < global_center.x < bbox.xmax - eps:
                candidates.append((global_center, normal, "SYMMETRY", 2.0))
            elif abs(normal.y) > 0.9 and bbox.ymin + eps < global_center.y < bbox.ymax - eps:
                candidates.append((global_center, normal, "SYMMETRY", 2.0))
            elif abs(normal.z) > 0.9 and bbox.zmin + eps < global_center.z < bbox.zmax - eps:
                candidates.append((global_center, normal, "SYMMETRY", 2.0))

        for hole in local_holes:
            c = cq.Vector(*hole["center"])
            r = hole.get("radius", 10)
            margin = r * 1.5
            for origin, normal in [
                (cq.Vector(c.x + margin, 0, 0), cq.Vector(1, 0, 0)),
                (cq.Vector(c.x - margin, 0, 0), cq.Vector(1, 0, 0)),
                (cq.Vector(0, c.y + margin, 0), cq.Vector(0, 1, 0)),
                (cq.Vector(0, c.y - margin, 0), cq.Vector(0, 1, 0))
            ]:
                if normal.x != 0 and bbox.xmin + eps < origin.x < bbox.xmax - eps:
                    candidates.append((origin, normal, "HOLE_ISO", 2.5))
                if normal.y != 0 and bbox.ymin + eps < origin.y < bbox.ymax - eps:
                    candidates.append((origin, normal, "HOLE_ISO", 2.5))

        for face in body.faces().vals():
            if self.classifier._get_face_type(face) == "Plane":
                n = face.normalAt(face.Center())
                if abs(n.z) > 0.9:
                    z = face.Center().z
                    if bbox.zmin + eps < z < bbox.zmax - eps:
                        candidates.append((cq.Vector(0, 0, z), cq.Vector(0, 0, 1), "STEP", 1.1))

        return self._unify_candidates(candidates)

    def _unify_candidates(self, candidates):
        if not candidates: return []
        unified = []
        for norm in [cq.Vector(1,0,0), cq.Vector(0,1,0), cq.Vector(0,0,1)]:
            group = [c for c in candidates if abs(c[1].dot(norm)) > 0.9]
            if not group: continue
            if norm.x > 0.9: group.sort(key=lambda x: x[0].x)
            elif norm.y > 0.9: group.sort(key=lambda x: x[0].y)
            else: group.sort(key=lambda x: x[0].z)
            
            current_cluster = [group[0]]
            threshold = 2.0 # Reverted to 2.0
            
            for next_cand in group[1:]:
                dist = 0
                if norm.x > 0.9: dist = abs(next_cand[0].x - current_cluster[-1][0].x)
                elif norm.y > 0.9: dist = abs(next_cand[0].y - current_cluster[-1][0].y)
                else: dist = abs(next_cand[0].z - current_cluster[-1][0].z)
                
                if dist < threshold: current_cluster.append(next_cand)
                else:
                    unified.append(max(current_cluster, key=lambda x: x[3]))
                    current_cluster = [next_cand]
            unified.append(max(current_cluster, key=lambda x: x[3]))
        return unified

    def _evaluate_candidate(self, body, candidate):
        origin, normal, ftype, weight = candidate
        try:
            parts = Splitter(body).apply_planar_split(origin, normal)
            if not parts or len(parts) < 2: return -1
            total_score = 0
            sliver_penalty = 0
            for p in parts:
                p_val = p.val()
                vol_ratio = p_val.Volume() / self.total_volume
                if vol_ratio < self.min_vol_ratio: sliver_penalty += 0.6
                res = self.validator.calculate_hex_readiness(p)
                total_score += res["total_score"]
            avg_score = total_score / len(parts)
            bbox = body.val().BoundingBox()
            dist = 0
            if abs(normal.x) > 0.9: dist = abs(origin.x - bbox.center.x) / (bbox.xlen / 2 + 0.1)
            elif abs(normal.y) > 0.9: dist = abs(origin.y - bbox.center.y) / (bbox.ylen / 2 + 0.1)
            elif abs(normal.z) > 0.9: dist = abs(origin.z - bbox.center.z) / (bbox.zlen / 2 + 0.1)
            centrality_bonus = 1.0 + (1.0 - dist) * 0.1
            return (avg_score * weight * centrality_bonus) * (1.0 - min(0.9, sliver_penalty))
        except: return -1

    def plan_and_execute(self):
        print(f"🛰️ Optimizing {self.model.val().hashCode()} (Limit: {self.max_bodies} bodies, {self.max_time}s)...")
        active_bodies = [self.model]
        iteration = 0
        used_planes = [] 

        def get_snapped_key(origin, normal, bodies):
            # [Expert] Keep #6: Snap-Aware Search, but using 1.0mm eps
            final_origin = origin
            snap_eps = 1.0
            for b in bodies:
                bbox = b.val().BoundingBox()
                if abs(normal.x) > 0.9:
                    if abs(bbox.xmin - origin.x) < snap_eps: final_origin = cq.Vector(bbox.xmin, origin.y, origin.z); break
                    elif abs(bbox.xmax - origin.x) < snap_eps: final_origin = cq.Vector(bbox.xmax, origin.y, origin.z); break
                elif abs(normal.y) > 0.9:
                    if abs(bbox.ymin - origin.y) < snap_eps: final_origin = cq.Vector(origin.x, bbox.ymin, origin.z); break
                    elif abs(bbox.ymax - origin.y) < snap_eps: final_origin = cq.Vector(origin.x, bbox.ymax, origin.z); break
            return (round(final_origin.x, 3), round(final_origin.y, 3), round(final_origin.z, 3),
                    round(normal.x, 3), round(normal.y, 3), round(normal.z, 3))

        while len(active_bodies) < self.max_bodies and iteration < 20:
            iteration += 1
            if time.time() - self.start_time > self.max_time: break
            
            best_plane = None
            best_overall_score = -1
            
            # Reverted: Pure Greedy search (No Symmetry-First)
            for body in active_bodies:
                candidates = self._generate_candidates(body, self._get_local_features(body))
                for cand in candidates:
                    origin, normal, ftype, weight = cand
                    # Keep #6: Snap-Aware Filtering
                    if get_snapped_key(origin, normal, active_bodies) in used_planes: continue
                    
                    score = self._evaluate_candidate(body, cand)
                    if score > best_overall_score:
                        best_overall_score = score
                        best_plane = cand
            
            if best_plane:
                origin, normal, ftype, _ = best_plane
                
                # Reverted: Local Snap logic (1.0mm)
                global_target_origin = origin
                for b in active_bodies:
                    bbox = b.val().BoundingBox()
                    if abs(normal.x) > 0.9:
                        if abs(bbox.xmin - origin.x) < self.snap_eps: global_target_origin = cq.Vector(bbox.xmin, origin.y, origin.z); break
                        elif abs(bbox.xmax - origin.x) < self.snap_eps: global_target_origin = cq.Vector(bbox.xmax, origin.y, origin.z); break
                    elif abs(normal.y) > 0.9:
                        if abs(bbox.ymin - origin.y) < self.snap_eps: global_target_origin = cq.Vector(origin.x, bbox.ymin, origin.z); break
                        elif abs(bbox.ymax - origin.y) < self.snap_eps: global_target_origin = cq.Vector(origin.x, bbox.ymax, origin.z); break
                
                plane_key = (round(global_target_origin.x, 3), round(global_target_origin.y, 3), round(global_target_origin.z, 3),
                             round(normal.x, 3), round(normal.y, 3), round(normal.z, 3))
                
                new_bodies = []
                any_split = False
                for i, b in enumerate(active_bodies):
                    # Reverted: Use _safe_split (Volume check > 0.1)
                    parts = self._safe_split(b, global_target_origin, normal)
                    if len(parts) > 1:
                        any_split = True
                        new_bodies.extend(parts)
                    else:
                        new_bodies.append(b)
                
                if any_split:
                    active_bodies = new_bodies
                    used_planes.append(plane_key)
                else:
                    used_planes.append(plane_key)
                    continue
            else: break

        finalized = []
        for b in active_bodies:
            if self._is_cylindrical_body(b) and len(finalized) + 4 <= self.max_bodies:
                try:
                    c = b.val().BoundingBox().center
                    q1 = self._safe_split(b, c, cq.Vector(1,0,0))
                    for q in q1: finalized.extend(self._safe_split(q, c, cq.Vector(0,1,0)))
                    continue
                except: pass
            finalized.append(b)
        return [b for b in finalized if b.val().Volume() > 0.1]

    def _is_cylindrical_body(self, body):
        return any(self.classifier._get_face_type(f) == "Cylinder" for f in body.faces().vals())

    def _safe_split(self, body, origin, normal):
        try:
            res = Splitter(body).apply_planar_split(origin, normal)
            if res:
                return [p for p in res if p.val().Volume() > 0.1]
        except: pass
        return [body]
