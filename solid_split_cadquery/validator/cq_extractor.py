import cadquery as cq
import os

def run_real_benchmark():
    test_files = [
        "validator/data/auto_cylinder.step",
        "validator/data/auto_stepped.step",
        "validator/data/auto_perforated.step",
        "validator/data/auto_curved.step"
    ]
    
    print(f"{'Target File':<25} | {'Status':<8} | {'Features':<10} | {'Result'}")
    print("-" * 70)

    for path in test_files:
        if not os.path.exists(path):
            continue
            
        try:
            # 1. 파일 읽기
            model = cq.importers.importStep(path)
            
            # 2. 모든 면을 가져와서 타입 확인
            all_faces = model.faces().vals()
            
            # 실린더형 면 개수 세기
            cyl_count = 0
            for f in all_faces:
                if "Cylinder" in str(type(f.wrapped)): # 명시적 타입 체크 지양, BRepAdaptor 권장하나 여기선 간단히
                    cyl_count += 1
            
            # 3. 바운딩 박스로 크기 확인 (가장 큰 면)
            main_face = max(all_faces, key=lambda f: f.BoundingBox().xlen)
            size = main_face.BoundingBox().xlen

            print(f"{os.path.basename(path):<25} | SUCCESS  | {len(all_faces):<10} | MaxDim: {size:.2f}")
        except Exception as e:
            print(f"{os.path.basename(path):<25} | ERROR    | {str(e)[:15]}")

if __name__ == "__main__":
    run_real_benchmark()
