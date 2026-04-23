import cadquery as cq
import numpy as np
import os

class ValidationEngine:
    def __init__(self, tolerance=1e-6):
        self.tolerance = tolerance

    def validate_split(self, original_model, split_results):
        """
        Perform a comprehensive validation of the splitting operation.
        """
        print("🔍 Starting Enhanced Validation Engine...")
        
        # 1. Volume Conservation Check
        original_vol = original_model.val().Volume()
        split_vol = sum(b.val().Volume() for b in split_results if b.val() is not None)
        vol_diff = abs(original_vol - split_vol)
        vol_pass = vol_diff < self.tolerance
        
        # 2. Hex-Readiness Scoring
        scores = []
        for i, body in enumerate(split_results):
            score_data = self.calculate_hex_readiness(body)
            scores.append(score_data)
            print(f" - Body {i} Hex Score: {score_data['total_score']:.1f} (Faces: {score_data['face_count']})")

        avg_hex_score = sum(s['total_score'] for s in scores) / len(scores) if scores else 0
        
        # 3. Interference Check
        interference_pass = True
        body_count = len(split_results)
        if body_count > 1:
            for i in range(body_count):
                for j in range(i + 1, body_count):
                    overlap = split_results[i].intersect(split_results[j])
                    if overlap.val() is not None and overlap.val().Volume() > self.tolerance:
                        interference_pass = False
        
        return {
            "volume": {
                "original": original_vol,
                "split": split_vol,
                "diff": vol_diff,
                "status": "PASS" if vol_pass else "FAIL"
            },
            "body_count": body_count,
            "interference": {"status": "PASS" if interference_pass else "FAIL"},
            "hex_readiness": {
                "average_score": avg_hex_score,
                "details": scores
            },
            "overall_status": "PASS" if (vol_pass and interference_pass) else "FAIL"
        }

    def calculate_hex_readiness(self, body):
        """
        Calculate a score (0-100) based on how easy it is to hex-mesh this body.
        """
        if body.val() is None: return {"total_score": 0}
        
        faces = body.faces().vals()
        face_count = len(faces)
        
        # 1. Face Count Score (Ideal = 6)
        # Penalty: 10 points for each face away from 6
        face_score = max(0, 100 - abs(face_count - 6) * 10)
        
        # 2. Orthogonality Score (Enhanced for Sweepable Curved Faces)
        ortho_score = 100
        try:
            normals = [f.normalAt(f.Center()) for f in faces]
            ortho_violations = 0
            for i, n1 in enumerate(normals):
                n1_np = np.array([n1.x, n1.y, n1.z])
                ortho_count = 0
                for j, n2 in enumerate(normals):
                    if i == j: continue
                    n2_np = np.array([n2.x, n2.y, n2.z])
                    dot = abs(np.dot(n1_np, n2_np))
                    # Standard orthogonal check (dot ~ 0 or 1)
                    if dot < 0.2: # Orthogonal
                        ortho_count += 1
                
                # [Expert Update] If it's a 6-faced body, allow for sweepable curved faces
                if face_count == 6:
                    # In a sweepable cylinder sector, you might have fewer than 4 perfect ortho neighbors
                    # but it's still highly meshable.
                    if ortho_count < 2: ortho_violations += 1
                else:
                    if ortho_count < 4: ortho_violations += 1
                    
            ortho_score = max(0, 100 - (ortho_violations * 10))
        except:
            ortho_score = 50 # Fallback
            
        # 3. Aspect Ratio Score
        try:
            bbox = body.val().BoundingBox()
            dims = sorted([bbox.xlen, bbox.ylen, bbox.zlen])
            aspect_ratio = dims[2] / dims[0] if dims[0] > 0 else 100
            aspect_score = max(0, 100 - (aspect_ratio - 1) * 5)
        except:
            aspect_ratio = 100
            aspect_score = 0

        # 4. Skewness Score (NEW)
        # 각 면의 법선벡터가 가장 가까운 주축(X/Y/Z)에서 벗어난 평균 각도
        # 0° = 완전 정렬(100점), 45° 이상 = 0점
        skewness_score = 100
        try:
            principal_axes = [
                np.array([1, 0, 0]),
                np.array([0, 1, 0]),
                np.array([0, 0, 1])
            ]
            deviations = []
            for f in faces:
                n = f.normalAt(f.Center())
                n_np = np.array([n.x, n.y, n.z])
                n_norm = np.linalg.norm(n_np)
                if n_norm < 1e-9:
                    continue
                n_np = n_np / n_norm
                # 가장 가까운 주축과의 각도 (절댓값으로 방향 무관하게 계산)
                min_dev = min(
                    np.degrees(np.arccos(np.clip(abs(np.dot(n_np, ax)), 0.0, 1.0)))
                    for ax in principal_axes
                )
                deviations.append(min_dev)
            if deviations:
                avg_deviation = np.mean(deviations)
                # 45° → 0점, 0° → 100점 (선형 보간)
                skewness_score = max(0.0, 100.0 - (avg_deviation / 45.0) * 100.0)
        except:
            skewness_score = 50  # Fallback

        # 가중치: face 35% / ortho 35% / aspect 15% / skewness 15%
        total_score = (face_score * 0.35) + (ortho_score * 0.35) + (aspect_score * 0.15) + (skewness_score * 0.15)

        return {
            "total_score": total_score,
            "face_count": face_count,
            "face_score": face_score,
            "ortho_score": ortho_score,
            "aspect_ratio": aspect_ratio,
            "aspect_score": aspect_score,
            "skewness_score": skewness_score
        }

if __name__ == "__main__":
    # Test with a simple split
    box = cq.Workplane("XY").box(10, 10, 10)
    split_a = box.intersect(cq.Workplane("XY").workplane(offset=0).box(10, 10, 10, centered=(True, True, False)))
    split_b = box.cut(cq.Workplane("XY").workplane(offset=0).box(10, 10, 10, centered=(True, True, False)))
    
    engine = ValidationEngine()
    result = engine.validate_split(box, [split_a, split_b])
    print("\n[Final Validation Result]")
    print(result)
