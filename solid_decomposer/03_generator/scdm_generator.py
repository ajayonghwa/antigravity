# -*- coding: utf-8 -*-
import os
import base64

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.output_dir = os.path.join(project_root, "04_scripts")
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir)
            except: self.output_dir = project_root

    def generate_script(self, plan_list, output_name="scdm_decomposition_script.py", units="mm"):
        unique_body_indices = sorted(list(set([p.get("body_index", 0) for p in plan_list])))
        body_index_to_name = {}
        for p in plan_list: body_index_to_name[p.get("body_index", 0)] = p.get("body_name", "Unknown")

        comp_creation_calls = ""
        for b_idx in unique_body_indices:
            bname = body_index_to_name[b_idx]
            bname_b64 = base64.b64encode(bname.encode('utf-8')).decode('ascii')
            comp_creation_calls += "create_body_component('{0}', {1})\n".format(bname_b64, b_idx)

        # [v4.81] 스케일 팩터 결정 (SCDM API는 항상 미터 단위)
        scale = 0.001 if units == "mm" else 1.0
        print(f" - Generator Scale: {scale} (Input units: {units})")

        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body_idx = plan.get("body_index", 0)
            body = plan.get("body_name", "Unknown")
            body_b64 = base64.b64encode(body.encode('utf-8')).decode('ascii')
            
            if strat in ["OGRID", "CGRID", "RADIAL_OFFSET"]:
                center = plan.get('center')
                if not center: continue
                
                import json as pyjson
                center_m = [float(c) * scale for c in center]
                axis = [float(a) for a in plan.get('axis', [0,0,1])]
                offset_m = float(plan.get('core_offset', 1.0)) * scale
                
                # [v4.84] 가독성을 위해 원본 바디 이름을 주석으로 추가
                if strat == "OGRID":
                    execution_calls += "apply_ogrid('{0}', {1}, {2}, {3}, {4}, {5})  # Target: {6}\n".format(body_b64, pyjson.dumps(center_m), pyjson.dumps(axis), offset_m, i, body_idx, body)
                elif strat == "CGRID":
                    wall_dir = [float(w) for w in plan.get('wall_direction', [0,0,1])]
                    execution_calls += "apply_cgrid('{0}', {1}, {2}, {3}, {4}, {5}, {6})  # Target: {7}\n".format(body_b64, pyjson.dumps(center_m), pyjson.dumps(axis), offset_m, pyjson.dumps(wall_dir), i, body_idx, body)
                elif strat == "RADIAL_OFFSET":
                    r_m = float(plan.get('split_radius', 1.0)) * scale
                    execution_calls += "apply_radial_offset('{0}', {1}, {2}, {3}, {4}, {5})  # Target: {6}\n".format(body_b64, pyjson.dumps(center_m), pyjson.dumps(axis), r_m, i, body_idx, body)
            
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                import json as pyjson
                split = plan.get("split_plane")
                if not split: continue
                origin_m = [float(o) * scale for o in split['origin']]
                normal = [float(n) for n in split.get('normal', [0,0,1])]
                execution_calls += "apply_split_plane('{0}', {1}, {2}, '{3}', {4}, {5})  # Target: {6}\n".format(body_b64, pyjson.dumps(origin_m), pyjson.dumps(normal), strat, i, body_idx, body)

        template = """# -*- coding: utf-8 -*-
# [v4.56] Standard Script Template
import math
import base64
import re
import clr

try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
except: pass

BODY_COMP_MAP = {}

def get_matching_bodies(body_b64):
    try: target_name = base64.b64decode(body_b64).decode('utf-8').lower().strip()
    except: target_name = body_b64.lower().strip()
    
    all_bodies = []
    try:
        # [v4.87] 추출기(Extractor)에서 검증된 로직 그대로 사용
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        
        desc = list(root.GetDescendants[IDesignBody]())
        for b in desc: all_bodies.append(b)
        
        # 하위 컴포넌트 내부 바디까지 샅샅이 뒤짐
        if not desc:
            for b in root.Bodies: all_bodies.append(b)
            for comp in root.Components:
                for b in comp.Template.Bodies: all_bodies.append(b)
    except: pass
    
    matched = []
    import re
    # [v4.89] 정규표현식을 사용한 정밀 매칭: [원본이름] + [숫자] 또는 [원본이름] 자체
    # 공백이나 특수문자를 제거한 상태에서 비교
    t_clean = target_name.replace(" ", "").replace("(", "").replace(")", "").replace("_", "")
    # 패턴: 시작이 t_clean이고 그 뒤에 숫자만 있거나 아무것도 없는 경우
    pattern = re.compile("^" + re.escape(t_clean) + r"\d*$")
    
    for b in all_bodies:
        b_name_clean = b.Name.lower().replace(" ", "").replace("(", "").replace(")", "").replace("_", "")
        if pattern.match(b_name_clean):
            matched.append(b)
    
    if not matched:
        print("   [WARN] No body or fragments found matching: {0}".format(target_name))
    else:
        print("   [INFO] Found {0} targets for '{1}'".format(len(matched), target_name))
    return matched

def create_body_component(name_b64, body_idx):
    global BODY_COMP_MAP
    root = GetRootPart()
    try: t_name = base64.b64decode(name_b64).decode('utf-8')
    except: t_name = name_b64
    comp_name = "CUTTERS_{0}".format(body_idx)
    target_comp = None
    for comp in root.Components:
        if comp.Name == comp_name: target_comp = comp; break
    if not target_comp:
        try:
            target_part = Part.Create(root.Document, comp_name)
            target_comp = Component.Create(root, target_part)
        except: pass
    BODY_COMP_MAP[body_idx] = target_comp

def _move_to_comp(obj, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try: ComponentHelper.MoveBodiesToComponent(Selection.Create(obj), target_comp)
    except: pass

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1] Start ogrid for {0}".format(targets[0].Name))
        origin_pt = Point.Create(center[0], center[1], center[2])
        direction = Direction.Create(axis[0], axis[1], axis[2])
        
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        
        bodies_before = list(root.GetDescendants[IDesignBody]())
        
        # [v4.97] O-Grid 원통형 생성
        try:
            frame = Frame.Create(origin_pt, direction)
            circle = Circle.Create(frame, offset)
            dc = DesignCurve.Create(root, CurveSegment.Create(circle))
            ExtrudeEdges.Execute(Selection.Create(dc.Edges[0]), None, MM(10000), None, None)
            print("   [DEBUG 2] ExtrudeEdges success")
        except Exception as ce:
            print("   [DEBUG 2-FAIL] ExtrudeEdges failed: " + str(ce))
            return

        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_b_list = [b for b in bodies_after if b not in bodies_before]
        
        if new_b_list:
            new_b = new_b_list[0]
            print("   [DEBUG 3] Starting split")
            try: SplitBody.ByCutter(Selection.Create(targets), Selection.Create(new_b.Faces[0]), True, None)
            except Exception as se: print("   [WARN] Split failed: " + str(se))
            _move_to_comp(new_b, b_idx)
        dc.Delete()
        print("   [OK] O-Grid complete for {0}".format(targets[0].Name))
    except Exception as e:
        print("   [ERROR] apply_ogrid crashed: " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1] Start split_plane for {0}".format(targets[0].Name))
        origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
        normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
        
        root = GetRootPart()
        if not root: root = Application.GetActiveDocument().MainPart
        
        print("   [DEBUG 2] Creating DatumPlane as Cutter")
        try:
            frame = Frame.Create(origin, normal)
            datum_plane = DatumPlane.Create(root, "Cutter_Plane", frame)
            print("   [DEBUG 3] DatumPlane success")
            
            try: 
                SplitBody.ByCutter(Selection.Create(targets), Selection.Create(datum_plane), True, None)
                print("   [DEBUG 4] Split by DatumPlane success")
            except Exception as se: 
                print("   [WARN] Split failed: " + str(se))
            
            _move_to_comp(datum_plane, b_idx)
            
        except Exception as de:
            print("   [DEBUG 3-FAIL] DatumPlane creation error: " + str(de))
            
        print("   [OK] {0} complete for {1}".format(strategy, targets[0].Name))
    except Exception as e:
        print("   [ERROR] apply_split_plane crashed: " + str(e))

REPLACE_COMP_CREATION
REPLACE_EXECUTION
print("Decomposition Finished.")
"""
        script_content = template.replace("REPLACE_COMP_CREATION", comp_creation_calls)
        script_content = script_content.replace("REPLACE_EXECUTION", execution_calls)
        
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f: f.write(script_content)
        return output_path
