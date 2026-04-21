import cadquery as cq
import os

def debug_read():
    path = "validator/data/auto_cylinder.step"
    if not os.path.exists(path):
        print("File not found")
        return

    print(f"Reading {path}...")
    try:
        # STEP 파일 읽기
        model = cq.importers.importStep(path)
        print(f"Model loaded: {type(model)}")
        
        # 실린더 면 개수만 확인
        cyls = model.faces("%Cylinder")
        print(f"Cylindrical faces: {len(cyls.vals())}")
        
        for i, face in enumerate(cyls.vals()):
            # 간단하게 바운딩 박스로 크기 확인
            bbox = face.BoundingBox()
            print(f" - Face {i+1} BBox: {bbox.xlen:.2f} x {bbox.ylen:.2f}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_read()
