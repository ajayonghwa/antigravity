import cadquery as cq
import os
import sys
import json
import numpy as np

# 프로젝트 루트 및 플래너 모듈 로드
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import importlib
planner_mod = importlib.import_module("02_planner.strategy_planner")
StrategyPlanner = planner_mod.StrategyPlanner

def extract_from_step(path):
    """STEP 파일에서 플래너가 이해할 수 있는 JSON 형식으로 데이터 추출 (정밀 축 정보 포함)"""
    model = cq.importers.importStep(path)
    body_data = {"body_name": os.path.basename(path), "faces": []}
    
    for face in model.faces().vals():
        f_type = "Unknown"
        try:
            gt = face.geomType().upper()
            if "CYLINDER" in gt: f_type = "Cylinder"
            elif "PLANE" in gt: f_type = "Plane"
            elif "CONE" in gt: f_type = "Conical"
            elif "TORUS" in gt: f_type = "Toroidal"
        except: pass
            
        center = face.Center()
        
        # [정밀화] 실린더의 실제 축 방향 추출
        axis = [0, 0, 1]
        try:
            if f_type == "Cylinder":
                # BRepAdaptor를 통한 축 정보 획득
                surf = face._geomAdaptor().Cylinder()
                ax = surf.Axis().Direction()
                axis = [ax.X(), ax.Y(), ax.Z()]
            elif f_type == "Conical":
                surf = face._geomAdaptor().Cone()
                ax = surf.Axis().Direction()
                axis = [ax.X(), ax.Y(), ax.Z()]
        except: pass

        data = {
            "type": f_type,
            "origin": [center.x, center.y, center.z],
            "axis": axis,
            "box": {
                "min": [face.BoundingBox().xmin, face.BoundingBox().ymin, face.BoundingBox().zmin],
                "max": [face.BoundingBox().xmax, face.BoundingBox().ymax, face.BoundingBox().zmax]
            }
        }
        
        if f_type in ["Cylinder", "Conical"]:
            try: data["radius"] = face.radius()
            except: data["radius"] = 10.0
            data["is_internal"] = face.wrapped.Orientation() == 1
            
        body_data["faces"].append(data)
    return body_data

def run_phase2_validation():
    planner = StrategyPlanner(sub_device_name="VIRTUAL_LAB_PHASE2")
    test_cases = [
        "validator/data/lv1_through_hole.step",
        "validator/data/lv1_blind_hole.step",
        "validator/data/lv1_taper_shaft.step",
        "validator/data/lv2_blind_hole_fillet.step",
        "validator/data/lv2_boss_plate.step",
        "validator/data/lv3_t_junction.step",
        "validator/data/lv4_final_boss.step",
        "validator/data/lv5_asymmetric_disk.step"
    ]
    
    print("🔬 [Virtual Lab: Phase 2] Testing Junction Recognition...")
    print("-" * 75)
    
    for path in test_cases:
        if not os.path.exists(path): continue
        print(f"\n[Testing: {os.path.basename(path)}]")
        body_data = extract_from_step(path)
        
        # 축 정보 확인 로그
        cyls = [f for f in body_data['faces'] if f['type'] == 'Cylinder']
        for i, c in enumerate(cyls):
            print(f" - Cyl {i} Axis: {c['axis']}, Radius: {c['radius']:.2f}")

        strategy, plans = planner.analyze_body(body_data)
        print(f" 🚀 Strategy Detected: {strategy}")
        if plans:
            print(f" 📦 Plans: {len(plans)} steps")

if __name__ == "__main__":
    run_phase2_validation()
