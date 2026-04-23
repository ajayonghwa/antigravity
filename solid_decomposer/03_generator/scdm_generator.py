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

# [v5.01] 명시적 참조 및 네임스페이스 충돌 방지
try:
    clr.AddReference("SpaceClaim.Api.V22")
    from SpaceClaim.Api.V22 import Application, Window, Selection, MM
    import SpaceClaim.Api.V22.Geometry as g
    import SpaceClaim.Api.V22.Modeler as m
    import SpaceClaim.Api.V22.Scripting.Selection as sel
    import SpaceClaim.Api.V22.Scripting.Commands as cmd
    import SpaceClaim.Api.V22.Scripting.Helpers as help
except Exception as ie:
    print("   [CRITICAL] Import failed: " + str(ie))

BODY_COMP_MAP = {}

def get_matching_bodies(body_b64):
    try: t_clean = base64.b64decode(body_b64).decode('utf-8').lower().strip()
    except: t_clean = body_b64.lower().strip()
    import re
    try:
        root = Application.GetActiveDocument().MainPart
        all_b = root.GetDescendants[m.IDesignBody]()
        pattern = re.compile("^" + re.escape(t_clean) + r"\\d*$")
        matches = [b for b in all_b if pattern.match(b.Name.lower().replace(" ", "")) or b.Name.lower() == t_clean]
        if matches: print("   [INFO] Found {0} targets for '{1}'".format(len(matches), t_clean))
        return matches
    except Exception as ge:
        print("   [ERROR] get_matching_bodies failed: " + str(ge))
        return []

def _init_comp(name_b64, body_idx):
    try:
        root = Application.GetActiveDocument().MainPart
        comp_name = "CUTTERS_{0}".format(body_idx)
        target_comp = next((c for c in root.Components if c.Name == comp_name), None)
        if not target_comp:
            target_part = m.Part.Create(root.Document, comp_name)
            target_comp = m.Component.Create(root, target_part)
        BODY_COMP_MAP[body_idx] = target_comp
    except Exception as ce:
        print("   [ERROR] _init_comp failed: " + str(ce))

def _move_to_comp(obj, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try: help.ComponentHelper.MoveBodiesToComponent(sel.Selection.Create(obj), target_comp)
    except: pass

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1] Start ogrid for {0}".format(targets[0].Name))
        # [v5.01] getattr를 사용하여 네임스페이스 에러 우회
        p_factory = g.Point
        d_factory = g.Direction
        origin_pt = getattr(p_factory, "Create")(MM(center[0]*1000), MM(center[1]*1000), MM(center[2]*1000))
        direction = getattr(d_factory, "Create")(axis[0], axis[1], axis[2])
        
        root = Application.GetActiveDocument().MainPart
        bodies_before = list(root.GetDescendants[m.IDesignBody]())
        
        try:
            ref = g.Direction.DirZ
            if abs(direction.Z) > 0.9: ref = g.Direction.DirX
            x_axis = g.Direction.Cross(direction, ref)
            frame = g.Frame.Create(origin_pt, direction, x_axis)
            circle = g.Circle.Create(frame, MM(offset*1000))
            dc = m.DesignCurve.Create(root, g.CurveSegment.Create(circle))
            
            cmd.ExtrudeEdges.Execute(sel.Selection.Create(dc.Edges[0]), origin_pt, direction, MM(10000), None, None)
            print("   [DEBUG 2] ExtrudeEdges success")
        except Exception as ce:
            print("   [DEBUG 2-FAIL] ExtrudeEdges failed: " + str(ce))
            return

        bodies_after = list(root.GetDescendants[m.IDesignBody]())
        new_b = next((b for b in bodies_after if b not in bodies_before), None)
        if new_b:
            print("   [DEBUG 3] Starting split")
            try: cmd.SplitBody.ByCutter(sel.Selection.Create(targets), sel.Selection.Create(new_b.Faces[0]), True, None)
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
        p_factory = g.Point
        d_factory = g.Direction
        origin = getattr(p_factory, "Create")(MM(origin_list[0]*1000), MM(origin_list[1]*1000), MM(origin_list[2]*1000))
        normal = getattr(d_factory, "Create")(normal_list[0], normal_list[1], normal_list[2])
        
        root = Application.GetActiveDocument().MainPart
        bodies_before = list(root.GetDescendants[m.IDesignBody]())
        
        try:
            ref = g.Direction.DirZ
            if abs(normal.Z) > 0.9: ref = g.Direction.DirX
            x_axis = g.Direction.Cross(normal, ref)
            frame = g.Frame.Create(origin, normal, x_axis)
            circle = g.Circle.Create(frame, MM(20000)) 
            dc = m.DesignCurve.Create(root, g.CurveSegment.Create(circle))
            
            try:
                cmd.Fill.Execute(sel.Selection.Create(dc.Edges[0]), None, None)
                print("   [DEBUG 3] Fill success")
            except:
                print("   [DEBUG 3-FAIL] Fill failed, trying DatumPlane")
                plane_obj = g.Plane.Create(frame)
                datum_plane = m.DatumPlane.Create(root, "Cutter_Plane", plane_obj)
                cmd.SplitBody.ByCutter(sel.Selection.Create(targets), sel.Selection.Create(datum_plane), True, None)
                _move_to_comp(datum_plane, b_idx)
                dc.Delete()
                return

            bodies_after = list(root.GetDescendants[m.IDesignBody]())
            new_b = next((b for b in bodies_after if b not in bodies_before), None)
            if new_b:
                print("   [DEBUG 4] Starting split")
                try: cmd.SplitBody.ByCutter(sel.Selection.Create(targets), sel.Selection.Create(new_b.Faces[0]), True, None)
                except Exception as se: print("   [WARN] Split failed: " + str(se))
                _move_to_comp(new_b, b_idx)
            dc.Delete()
        except Exception as de:
            print("   [DEBUG 3-FAIL] Cutter creation error: " + str(de))
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
