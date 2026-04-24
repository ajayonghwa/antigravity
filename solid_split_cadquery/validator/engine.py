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
        Calculate a score (0-100) based on Primitive Fidelity.
        Score is 100 if the body is a Box, Cylinder, Hollow Cylinder, or their 1/2-1/4 Sectors.
        """
        from core.classifier import Classifier
        classifier = Classifier(None)
        
        primitive_type = classifier.is_primitive(body)
        
        if primitive_type:
            total_score = 100.0
        else:
            # Fallback for non-primitives: give a low score based on face count
            faces = body.faces().vals()
            total_score = max(0, 50 - abs(len(faces) - 6) * 5)
            
        return {
            "total_score": total_score,
            "primitive_type": primitive_type,
            "face_count": len(body.faces().vals())
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
