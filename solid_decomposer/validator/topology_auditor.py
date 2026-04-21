import cadquery as cq
import os
import numpy as np

def audit_topology(step_path):
    if not os.path.exists(step_path): return
    print(f"\n[Deep Auditing] {step_path}")
    model = cq.importers.importStep(step_path)
    cyl_faces = model.faces("%Cylinder").vals()
    
    for i, face in enumerate(cyl_faces):
        # 1. 면의 기하학적 중심 (Center of Mass)
        cp = face.Center()
        
        # 2. 중심(0,0)에서 표면으로 향하는 방향 벡터 (Radial)
        # (원기둥이 원점에 있다고 가정)
        radial_vec = np.array([cp.x, cp.y])
        
        # 3. 해당 지점에서의 법선 벡터 (Normal)
        normal = face.normalAt(cp)
        normal_vec = np.array([normal.x, normal.y])
        
        # 4. 내적 판별
        dot = np.dot(radial_vec, normal_vec)
        is_hole = dot < 0
        
        status = "INTERNAL (HOLE)" if is_hole else "EXTERNAL (SOLID)"
        print(f" - Feature {i+1}: {status} (Dot Product: {dot:.4f})")
        print(f"   ㄴ Evidence: Normal is pointing {'INWARD' if is_hole else 'OUTWARD'}.")

if __name__ == "__main__":
    audit_topology("validator/data/auto_perforated.step")
