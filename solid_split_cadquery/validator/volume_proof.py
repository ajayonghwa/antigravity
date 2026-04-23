import os
import numpy as np
import cadquery as cq

def run_full_audit():
    test_cases = [
        {"name": "auto_cylinder.step", "type": "Solid"},
        {"name": "auto_stepped.step", "type": "Solid"},
        {"name": "auto_perforated.step", "type": "Hollow/Perforated"},
        {"name": "auto_curved.step", "type": "Curved"}
    ]
    
    print(f"{'Target Model':<25} | {'Measured Vol':<15} | {'Topological Status'}")
    print("-" * 65)

    for case in test_cases:
        path = os.path.join("validator/data", case["name"])
        if not os.path.exists(path): continue
        
        model = cq.importers.importStep(path)
        vol = model.val().Volume()
        
        # 위상 검사: 실린더 면들 중 '내경(Hole)'이 존재하는지 체크
        cyl_faces = model.faces("%Cylinder").vals()
        has_hole = False
        for f in cyl_faces:
            # 원점에서 바깥쪽으로 향하는 벡터와 법선 벡터 비교
            cp = f.Center()
            radial = np.array([cp.x, cp.y, 0])
            try:
                norm = f.normalAt(cp)
                normal = np.array([norm.x, norm.y, 0])
                if np.dot(radial, normal) < -0.1: # 안쪽을 향하면 구멍
                    has_hole = True
                    break
            except: pass

        status = "HOLES DETECTED" if has_hole else "PURE SOLID"
        print(f"{case['name']:<25} | {vol:>12.1f} | {status}")

if __name__ == "__main__":
    run_full_audit()
