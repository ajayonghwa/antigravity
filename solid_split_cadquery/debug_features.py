import os
import cadquery as cq
from core.classifier import Classifier

def debug_features():
    model_path = "input/lv4_final_boss.step"
    model = cq.importers.importStep(model_path)
    classifier = Classifier(model)
    report = classifier.get_feature_report()
    
    print("\n--- DEBUG REPORT: lv4_final_boss ---")
    print(f"Total Cylindrical Faces: {len(report['holes'])}")
    for i, hole in enumerate(report['holes']):
        print(f"Feature {i}:")
        print(f"  Center: {hole['center']}")
        print(f"  Internal: {hole['is_internal']}")
        print(f"  WHR: {hole['whr']}")
    
    # Check all faces
    faces = model.faces().vals()
    print(f"\nTotal Faces in model: {len(faces)}")
    for i, face in enumerate(faces):
        geom = face.wrapped.Surface().Value()
        # Check if it's cylindrical
        from OCP.Geom import Geom_CylindricalSurface
        if isinstance(geom, Geom_CylindricalSurface):
            print(f"Face {i} is Cylindrical")

if __name__ == "__main__":
    debug_features()
