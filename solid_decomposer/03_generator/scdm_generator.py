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
            comp_creation_calls += "_init_comp('{0}', {1})\n".format(bname_b64, b_idx)

        scale = 0.001 if units == "mm" else 1.0
        print(f" - Generator Scale: {scale} (Input units: {units})")

        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body_idx = plan.get("body_index", 0)
            body = plan.get("body_name", "Unknown")
            body_b64 = base64.b64encode(body.encode('utf-8')).decode('ascii')
            
            import json as pyjson
            if strat in ["OGRID", "CGRID", "RADIAL_OFFSET"]:
                center_m = [float(c) * scale for c in plan.get('center', [0,0,0])]
                axis = [float(a) for a in plan.get('axis', [0,0,1])]
                offset_m = float(plan.get('core_offset', 1.0)) * scale
                if strat == "OGRID":
                    execution_calls += "apply_ogrid('{0}', {1}, {2}, {3}, {4}, {5})  # Target: {6}\n".format(body_b64, pyjson.dumps(center_m), pyjson.dumps(axis), offset_m, i, body_idx, body)
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan.get("split_plane")
                if not split: continue
                origin_m = [float(o) * scale for o in split['origin']]
                normal = [float(n) for n in split.get('normal', [0,0,1])]
                execution_calls += "apply_split_plane('{0}', {1}, {2}, '{3}', {4}, {5})  # Target: {6}\n".format(body_b64, pyjson.dumps(origin_m), pyjson.dumps(normal), strat, i, body_idx, body)

        template = """# -*- coding: utf-8 -*-
import base64
import json as pyjson
import clr
import re

# [v5.08] Clean Reversion
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import *
    from SpaceClaim.Api.V22.Modeler import *
    from SpaceClaim.Api.V22.Geometry import *
    from SpaceClaim.Api.V22.Scripting import *
except: pass

BODY_COMP_MAP = {}

def get_matching_bodies(body_b64):
    try: t_clean = base64.b64decode(body_b64).decode('utf-8').lower().strip()
    except: t_clean = body_b64.lower().strip()
    try:
        # [v5.03] 가장 안정적인 활성 문서 접근 방식 사용
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        all_b = root.GetDescendants[IDesignBody]()
        pattern = re.compile("^" + re.escape(t_clean) + r"\\d*$")
        matches = [b for b in all_b if pattern.match(b.Name.lower().replace(" ", "")) or b.Name.lower() == t_clean]
        if matches: print("   [INFO] Found {0} targets for '{1}'".format(len(matches), t_clean))
        return matches
    except Exception as ge:
        print("   [ERROR] get_matching_bodies failed: " + str(ge))
        return []

def _init_comp(name_b64, body_idx):
    try:
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        comp_name = "CUTTERS_{0}".format(body_idx)
        target_comp = next((c for c in root.Components if c.Name == comp_name), None)
        if not target_comp:
            target_part = Part.Create(doc, comp_name)
            target_comp = Component.Create(root, target_part)
        BODY_COMP_MAP[body_idx] = target_comp
    except Exception as ce:
        print("   [ERROR] _init_comp failed: " + str(ce))

def _move_to_comp(obj, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try: ComponentHelper.MoveBodiesToComponent(Selection.Create(obj), target_comp)
    except: pass

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1.0] Start ogrid for {0}".format(targets[0].Name))
        origin_pt = Point.Create(MM(center[0]*1000), MM(center[1]*1000), MM(center[2]*1000))
        direction = Direction.Create(axis[0], axis[1], axis[2])
        
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        bodies_before = list(root.GetDescendants[IDesignBody]())
        
        try:
            # [v5.17] 삐뚤어짐 방지: Z축(direction)과 보조 X축을 활용하여 프레임을 명시적으로 생성
            # World X축과 평행하지 않은 경우 World X를 참조축으로 사용
            ref_x = Direction.DirX if abs(axis[0]) < 0.9 else Direction.DirY
            temp_frame = Frame.Create(origin_pt, direction, ref_x)
            
            circle = Circle.Create(temp_frame, MM(offset*1000))
            dc = DesignCurve.Create(root, CurveSegment.Create(circle))
            print("   [DEBUG 1.4] Curve aligned and created")
            
            sel_class = SpaceClaim.Api.V22.Scripting.Selection.Selection
            sel_obj = sel_class.Create(dc)
            
            options = ExtrudeEdgeOptions()
            # [v5.17] 안정적 압출: 방향 벡터를 정규화하여 전달
            ExtrudeEdges.Execute(sel_obj, direction, MM(10000), options, None)
            print("   [DEBUG 2.0] ExtrudeEdges success")
        except Exception as ce:
            print("   [DEBUG 2-FAIL] Sub-step failed: " + str(ce))
            return

        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_b = next((b for b in bodies_after if b not in bodies_before), None)
        if new_b:
            try: 
                target_sel = sel_class.Create(targets)
                cutter_faces = new_b.GetDescendants[IDesignFace]()
                cutter_sel = sel_class.Create(cutter_faces)
                SplitBody.ByCutter(target_sel, cutter_sel, True, None)
                print("   [DEBUG 3.0] SplitBody success")
            except Exception as se: print("   [WARN] Split failed: " + str(se))
            _move_to_comp(new_b, b_idx)
        dc.Delete()
    except Exception as e:
        print("   [ERROR] apply_ogrid crashed: " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1.0] Start split_plane for {0}".format(targets[0].Name))
        origin = Point.Create(MM(origin_list[0]*1000), MM(origin_list[1]*1000), MM(origin_list[2]*1000))
        normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
        
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        
        # [v5.17] 평면 분할 시에는 가장 Stable한 DatumPlane 방식을 우선 사용
        try:
            ref_x = Direction.DirX if abs(normal_list[0]) < 0.9 else Direction.DirY
            temp_frame = Frame.Create(origin, normal, ref_x)
            plane_obj = Plane.Create(temp_frame)
            datum_plane = DatumPlane.Create(root, "Cutter_Plane", plane_obj)
            
            sel_class = SpaceClaim.Api.V22.Scripting.Selection.Selection
            SplitBody.ByCutter(sel_class.Create(targets), sel_class.Create(datum_plane), True, None)
            _move_to_comp(datum_plane, b_idx)
            print("   [OK] {0} with DatumPlane complete".format(strategy))
        except Exception as de:
            print("   [DEBUG 3-FAIL] Stable split failed, trying fallback: " + str(de))
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
