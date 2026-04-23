import cadquery as cq
import os
import numpy as np
import time
from .splitter import Splitter
from .classifier import Classifier
from validator.engine import ValidationEngine

class StrategyPlanner:
    def __init__(self, model, max_bodies=40, max_time=15, target_score=85, min_vol_ratio=0.02):
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
        self.total_volume = model.val().Volume()

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
        eps = 2.0 # Increased epsilon to prevent thin slivers
        
        # Priority 1: Global Symmetry
        global_center = cq.Vector(*self.global_report.get("center", [0,0,0]))
        for normal in [cq.Vector(1,0,0), cq.Vector(0,1,0), cq.Vector(0,0,1)]:
            if abs(normal.x) > 0.9 and bbox.xmin + eps < global_center.x < bbox.xmax - eps:
                candidates.append((global_center, normal, "SYMMETRY", 2.0))
            elif abs(normal.y) > 0.9 and bbox.ymin + eps < global_center.y < bbox.ymax - eps:
                candidates.append((global_center, normal, "SYMMETRY", 2.0))
            elif abs(normal.z) > 0.9 and bbox.zmin + eps < global_center.z < bbox.zmax - eps:
                candidates.append((global_center, normal, "SYMMETRY", 2.0))

        # Priority 2: Hole Isolation
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
                    candidates.append((origin, normal, "HOLE_ISO", 1.5))
                if normal.y != 0 and bbox.ymin + eps < origin.y < bbox.ymax - eps:
                    candidates.append((origin, normal, "HOLE_ISO", 1.5))

        # Priority 3: Steps
        for face in body.faces().vals():
            if self.classifier._get_face_type(face) == "Plane":
                n = face.normalAt(face.Center())
                if abs(n.z) > 0.9:
                    z = face.Center().z
                    if bbox.zmin + eps < z < bbox.zmax - eps:
                        candidates.append((cq.Vector(0, 0, z), cq.Vector(0, 0, 1), "STEP", 1.1))

        return self._unify_candidates(candidates)

    def _unify_candidates(self, candidates):
        """Merge candidates that are too close to each other to prevent clustering"""
        if not candidates: return []
        
        unified = []
        # Group by normal (X, Y, Z)
        for norm in [cq.Vector(1,0,0), cq.Vector(0,1,0), cq.Vector(0,0,1)]:
            group = [c for c in candidates if abs(c[1].dot(norm)) > 0.9]
            if not group: continue
            
            # Sort by coordinate along the normal
            if norm.x > 0.9: group.sort(key=lambda x: x[0].x)
            elif norm.y > 0.9: group.sort(key=lambda x: x[0].y)
            else: group.sort(key=lambda x: x[0].z)
            
            # Merge logic
            if not group: continue
            current_cluster = [group[0]]
            
            threshold = 5.0 # Minimum 5mm distance between parallel planes
            
            for next_cand in group[1:]:
                dist = 0
                if norm.x > 0.9: dist = abs(next_cand[0].x - current_cluster[-1][0].x)
                elif norm.y > 0.9: dist = abs(next_cand[0].y - current_cluster[-1][0].y)
                else: dist = abs(next_cand[0].z - current_cluster[-1][0].z)
                
                if dist < threshold:
                    current_cluster.append(next_cand)
                else:
                    # Pick the best from the cluster (highest weight)
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
                # Global Volume Ratio Penalty (Sliver prevention)
                vol_ratio = p_val.Volume() / self.total_volume
                if vol_ratio < self.min_vol_ratio: 
                    sliver_penalty += 0.6 # Heavy penalty
                
                res = self.validator.calculate_hex_readiness(p)
                total_score += res["total_score"]
            
            avg_score = total_score / len(parts)
            
            # Centrality Bonus
            bbox = body.val().BoundingBox()
            dist = 0
            if abs(normal.x) > 0.9: dist = abs(origin.x - bbox.center.x) / (bbox.xlen / 2 + 0.1)
            elif abs(normal.y) > 0.9: dist = abs(origin.y - bbox.center.y) / (bbox.ylen / 2 + 0.1)
            elif abs(normal.z) > 0.9: dist = abs(origin.z - bbox.center.z) / (bbox.zlen / 2 + 0.1)
            centrality_bonus = 1.0 + (1.0 - dist) * 0.1
            
            final_score = (avg_score * weight * centrality_bonus) * (1.0 - min(0.9, sliver_penalty))
            return final_score
        except:
            return -1

    def plan_and_execute(self):
        """[User-Controlled Engine]"""
        print(f"🛰️ Optimizing {self.model.val().hashCode()} (Limit: {self.max_bodies} bodies, {self.max_time}s)...")
        
        active_bodies = [self.model]
        iteration = 0
        
        while len(active_bodies) < self.max_bodies and iteration < 20:
            iteration += 1
            if time.time() - self.start_time > self.max_time:
                print("⏱️ Time limit reached.")
                break
                
            # Early Exit: If average score is good enough
            current_total = sum(self.validator.calculate_hex_readiness(b)["total_score"] for b in active_bodies)
            avg_current = current_total / len(active_bodies)
            if avg_current >= self.target_score:
                print(f"✨ Target score reached ({avg_current:.1f}).")
                break
            
            best_plane = None
            best_overall_score = -1
            
            for body in active_bodies:
                candidates = self._generate_candidates(body, self._get_local_features(body))
                for cand in candidates:
                    score = self._evaluate_candidate(body, cand)
                    if score > best_overall_score:
                        best_overall_score = score
                        best_plane = cand
            
            if best_plane and best_overall_score > avg_current * 1.1:
                origin, normal, ftype, _ = best_plane
                print(f"   [{iteration}] Global Split: {ftype} (Score: {best_overall_score:.1f}, Bodies: {len(active_bodies)})")
                
                new_bodies = []
                for b in active_bodies:
                    bbox = b.val().BoundingBox()
                    intersects = False
                    if abs(normal.x) > 0.9 and bbox.xmin < origin.x < bbox.xmax: intersects = True
                    elif abs(normal.y) > 0.9 and bbox.ymin < origin.y < bbox.ymax: intersects = True
                    elif abs(normal.z) > 0.9 and bbox.zmin < origin.z < bbox.zmax: intersects = True
                    
                    if intersects:
                        new_bodies.extend(self._safe_split(b, origin, normal))
                    else:
                        new_bodies.append(b)
                active_bodies = new_bodies
            else:
                break

        # Final Sector Pass (Only if it doesn't exceed body limit)
        finalized = []
        for b in active_bodies:
            if self._is_cylindrical_body(b) and len(finalized) + 4 <= self.max_bodies:
                try:
                    c = b.val().BoundingBox().center
                    q1 = Splitter(b).apply_planar_split(c, cq.Vector(1,0,0))
                    for q in q1:
                        finalized.extend(Splitter(q).apply_planar_split(c, cq.Vector(0,1,0)))
                    continue
                except: pass
            finalized.append(b)

        return [b for b in finalized if b.val().Volume() > 0.1]

    def _is_cylindrical_body(self, body):
        return any(self.classifier._get_face_type(f) == "Cylinder" for f in body.faces().vals())

    def _safe_split(self, body, origin, normal):
        try:
            res = Splitter(body).apply_planar_split(origin, normal)
            if res: return [p for p in res if p.val().Volume() > 0.1]
        except: pass
        return [body]
