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

# [v5.18] stable_v1_backup의 무적 API 초기화 로직 복원
def initialize_api():
    for v in range(22, 16, -1):
        try:
            ref = "SpaceClaim.Api.V" + str(v)
            clr.AddReference(ref)
            exec("from SpaceClaim.Api.V" + str(v) + " import *", globals())
            exec("from SpaceClaim.Api.V" + str(v) + ".Modeler import *", globals())
            exec("from SpaceClaim.Api.V" + str(v) + ".Commands import *", globals())
            exec("from SpaceClaim.Api.V" + str(v) + ".Geometry import *", globals())
            exec("from SpaceClaim.Api.V" + str(v) + ".Scripting import *", globals())
            return True
        except: pass
    return False

initialize_api()

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
    for target_body in targets:
        try:
            print("   [DEBUG] O-Grid Start for " + target_body.Name)
            origin_pt = Point.Create(MM(center[0]*1000), MM(center[1]*1000), MM(center[2]*1000))
            direction = Direction.Create(axis[0], axis[1], axis[2])
            
            # [v5.18] stable_v1의 오프셋 관통 로직: 커브를 뒤로 100mm 밀어서 압출
            shifted_origin = Point.Create(origin_pt.X - direction.X * MM(100), 
                                          origin_pt.Y - direction.Y * MM(100), 
                                          origin_pt.Z - direction.Z * MM(100))
            
            ref_x = Direction.DirX if abs(axis[0]) < 0.9 else Direction.DirY
            temp_frame = Frame.Create(shifted_origin, direction, ref_x)
            circle = Circle.Create(temp_frame, MM(offset*1000))
            
            root = Window.ActiveWindow.Document.MainPart
            
            # [v5.19] ITrimmedCurve 형변환 에러 해결: .AsTrimmedCurve() 명시적 호출
            try:
                geom = CurveSegment.Create(circle).AsTrimmedCurve()
                dc = DesignCurve.Create(root, geom)
            except:
                try:
                    dc = DesignCurve.Create(root, CurveSegment.Create(circle))
                except:
                    dc = DesignCurve.Create(root, circle.AsTrimmedCurve())
            
            print("   [DEBUG] DesignCurve created")
            
            tool_body = None
            bodies_before = list(root.GetDescendants[IDesignBody]())
            sel = SpaceClaim.Api.V22.Scripting.Selection.Selection.Create(dc)
            
            extrude_dist = MM(10000)
            try:
                # [v5.18] 다단계 Extrude 시도 (4인자 -> 5인자)
                try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
                except: ExtrudeEdges.Execute(sel, direction, extrude_dist, ExtrudeEdgeOptions(), None)
            except:
                # [v5.18] 최후의 보루: Pull 도구 시도
                try: Pull.Execute(sel, direction, extrude_dist, PullOptions(), None)
                except: pass
            
            bodies_after = list(root.GetDescendants[IDesignBody]())
            new_bodies = [b for b in bodies_after if b not in bodies_before]
            
            if new_bodies:
                tool_body = new_bodies[0]
                target_sel = SpaceClaim.Api.V22.Scripting.Selection.Selection.Create(target_body)
                cutter_sel = SpaceClaim.Api.V22.Scripting.Selection.Selection.Create(tool_body.Faces)
                SplitBody.ByCutter(target_sel, cutter_sel, True, None)
                print("   [DEBUG] SplitBody success")
            
            _move_to_comp(tool_body, b_idx)
            dc.Delete()
            print("   [OK] O-Grid Success")
        except Exception as e:
            print("   [ERROR] O-Grid fail: " + str(e))

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    for target in targets:
        try:
            print("   [DEBUG] Split Start for " + target.Name)
            origin = Point.Create(MM(origin_list[0]*1000), MM(origin_list[1]*1000), MM(origin_list[2]*1000))
            normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
            
            ref_x = Direction.DirX if abs(normal_list[0]) < 0.9 else Direction.DirY
            temp_frame = Frame.Create(origin, normal, ref_x)
            plane_obj = Plane.Create(temp_frame)
            
            root = Window.ActiveWindow.Document.MainPart
            datum_plane = DatumPlane.Create(root, "Cutter_Plane", plane_obj)
            
            sel_class = SpaceClaim.Api.V22.Scripting.Selection.Selection
            SplitBody.ByCutter(sel_class.Create(target), sel_class.Create(datum_plane), True, None)
            _move_to_comp(datum_plane, b_idx)
            print("   [OK] {0} Success".format(strategy))
        except Exception as e:
            print("   [ERROR] Split fail: " + str(e))

REPLACE_COMP_CREATION
REPLACE_EXECUTION
print("Decomposition Finished.")
"""
        script_content = template.replace("REPLACE_COMP_CREATION", comp_creation_calls)
        script_content = script_content.replace("REPLACE_EXECUTION", execution_calls)
        
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f: f.write(script_content)
        return output_path
