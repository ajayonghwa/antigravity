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

# [v5.06] Absolute Robustness Architecture
import clr
try:
    clr.AddReference("SpaceClaim.Api.V22")
    import SpaceClaim.Api.V22 as api_mod
    import SpaceClaim.Api.V22.Geometry as geom_mod
    import SpaceClaim.Api.V22.Modeler as model_mod
    import SpaceClaim.Api.V22.Scripting.Selection as sel_mod
    import SpaceClaim.Api.V22.Scripting.Commands as cmd_mod
    import SpaceClaim.Api.V22.Scripting.Helpers as help_mod
    
    # [v5.06] 자체 MM 함수 구현 (SCDM 내부 단위는 항상 미터)
    def MM(val): return float(val) / 1000.0
    
    # 필수 전역 객체 획득
    Application = getattr(api_mod, "Application")
    Window = getattr(api_mod, "Window")
except Exception as ie:
    print("   [CRITICAL] Module loading failed: " + str(ie))

BODY_COMP_MAP = {}

def get_matching_bodies(body_b64):
    try: t_clean = base64.b64decode(body_b64).decode('utf-8').lower().strip()
    except: t_clean = body_b64.lower().strip()
    import re
    try:
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        idb_type = getattr(model_mod, "IDesignBody")
        all_b = root.GetDescendants[idb_type]()
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
            part_class = getattr(model_mod, "Part")
            comp_class = getattr(model_mod, "Component")
            target_part = getattr(part_class, "Create")(doc, comp_name)
            target_comp = getattr(comp_class, "Create")(root, target_part)
        BODY_COMP_MAP[body_idx] = target_comp
    except Exception as ce:
        print("   [ERROR] _init_comp failed: " + str(ce))

def _move_to_comp(obj, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try: 
        ch_class = getattr(help_mod, "ComponentHelper")
        s_class = getattr(sel_mod, "Selection")
        getattr(ch_class, "MoveBodiesToComponent")(getattr(s_class, "Create")(obj), target_comp)
    except: pass

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1] Start ogrid for {0}".format(targets[0].Name))
        p_factory = getattr(geom_mod, "Point")
        d_factory = getattr(geom_mod, "Direction")
        origin_pt = getattr(p_factory, "Create")(MM(center[0]*1000), MM(center[1]*1000), MM(center[2]*1000))
        direction = getattr(d_factory, "Create")(axis[0], axis[1], axis[2])
        
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        idb_type = getattr(model_mod, "IDesignBody")
        bodies_before = list(root.GetDescendants[idb_type]())
        
        try:
            ref = getattr(d_factory, "DirZ")
            if abs(direction.Z) > 0.9: ref = getattr(d_factory, "DirX")
            x_axis = getattr(d_factory, "Cross")(direction, ref)
            frame = getattr(getattr(geom_mod, "Frame"), "Create")(origin_pt, direction, x_axis)
            circle = getattr(getattr(geom_mod, "Circle"), "Create")(frame, MM(offset*1000))
            dc = getattr(getattr(model_mod, "DesignCurve"), "Create")(root, getattr(getattr(geom_mod, "CurveSegment"), "Create")(circle))
            
            sel_class = getattr(sel_mod, "Selection")
            getattr(getattr(cmd_mod, "ExtrudeEdges"), "Execute")(getattr(sel_class, "Create")(dc.Edges[0]), origin_pt, direction, MM(10000), None, None)
            print("   [DEBUG 2] ExtrudeEdges success")
        except Exception as ce:
            print("   [DEBUG 2-FAIL] ExtrudeEdges failed: " + str(ce))
            return

        bodies_after = list(root.GetDescendants[idb_type]())
        new_b = next((b for b in bodies_after if b not in bodies_before), None)
        if new_b:
            print("   [DEBUG 3] Starting split")
            s_class = getattr(sel_mod, "Selection")
            try: getattr(getattr(cmd_mod, "SplitBody"), "ByCutter")(getattr(s_class, "Create")(targets), getattr(s_class, "Create")(new_b.Faces[0]), True, None)
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
        p_factory = getattr(geom_mod, "Point")
        d_factory = getattr(geom_mod, "Direction")
        origin = getattr(p_factory, "Create")(MM(origin_list[0]*1000), MM(origin_list[1]*1000), MM(origin_list[2]*1000))
        normal = getattr(d_factory, "Create")(normal_list[0], normal_list[1], normal_list[2])
        
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        idb_type = getattr(model_mod, "IDesignBody")
        bodies_before = list(root.GetDescendants[idb_type]())
        
        try:
            ref = getattr(d_factory, "DirZ")
            if abs(normal.Z) > 0.9: ref = getattr(d_factory, "DirX")
            x_axis = getattr(d_factory, "Cross")(normal, ref)
            frame = getattr(getattr(geom_mod, "Frame"), "Create")(origin, normal, x_axis)
            circle = getattr(getattr(geom_mod, "Circle"), "Create")(frame, MM(20000)) 
            dc = getattr(getattr(model_mod, "DesignCurve"), "Create")(root, getattr(getattr(geom_mod, "CurveSegment"), "Create")(circle))
            
            s_class = getattr(sel_mod, "Selection")
            try:
                getattr(getattr(cmd_mod, "Fill"), "Execute")(getattr(s_class, "Create")(dc.Edges[0]), None, None)
                print("   [DEBUG 3] Fill success")
            except:
                print("   [DEBUG 3-FAIL] Fill failed, trying DatumPlane")
                plane_obj = getattr(getattr(geom_mod, "Plane"), "Create")(frame)
                datum_plane = getattr(getattr(model_mod, "DatumPlane"), "Create")(root, "Cutter_Plane", plane_obj)
                getattr(getattr(cmd_mod, "SplitBody"), "ByCutter")(getattr(s_class, "Create")(targets), getattr(s_class, "Create")(datum_plane), True, None)
                _move_to_comp(datum_plane, b_idx)
                dc.Delete()
                return

            bodies_after = list(root.GetDescendants[idb_type]())
            new_b = next((b for b in bodies_after if b not in bodies_before), None)
            if new_b:
                print("   [DEBUG 4] Starting split")
                try: getattr(getattr(cmd_mod, "SplitBody"), "ByCutter")(getattr(s_class, "Create")(targets), getattr(s_class, "Create")(new_b.Faces[0]), True, None)
                except Exception as se: print("   [WARN] Split failed: " + str(se))
                _move_to_comp(new_b, b_idx)
            dc.Delete()
        except Exception as de:
            print("   [DEBUG 3-FAIL] Cutter creation error: " + str(de))
        print("   [OK] {0} complete for {1}".format(strategy, targets[0].Name))
    except Exception as e:
        print("   [ERROR] apply_split_plane crashed: " + str(e))

BODY_COMP_MAP = {}

def get_matching_bodies(body_b64):
    try: t_clean = base64.b64decode(body_b64).decode('utf-8').lower().strip()
    except: t_clean = body_b64.lower().strip()
    import re
    try:
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        # [v5.04] getattr를 사용하여 IDesignBody 타입 추출
        idb_type = getattr(model_mod, "IDesignBody")
        all_b = root.GetDescendants[idb_type]()
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
            # [v5.04] getattr를 사용하여 Part/Component 타입 추출
            part_class = getattr(model_mod, "Part")
            comp_class = getattr(model_mod, "Component")
            target_part = getattr(part_class, "Create")(doc, comp_name)
            target_comp = getattr(comp_class, "Create")(root, target_part)
        BODY_COMP_MAP[body_idx] = target_comp
    except Exception as ce:
        print("   [ERROR] _init_comp failed: " + str(ce))

def _move_to_comp(obj, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try: 
        ch_class = getattr(help_mod, "ComponentHelper")
        s_class = getattr(sel_mod, "Selection")
        getattr(ch_class, "MoveBodiesToComponent")(getattr(s_class, "Create")(obj), target_comp)
    except: pass

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    try:
        print("   [DEBUG 1] Start ogrid for {0}".format(targets[0].Name))
        p_factory = getattr(geom_mod, "Point")
        d_factory = getattr(geom_mod, "Direction")
        origin_pt = getattr(p_factory, "Create")(MM(center[0]*1000), MM(center[1]*1000), MM(center[2]*1000))
        direction = getattr(d_factory, "Create")(axis[0], axis[1], axis[2])
        
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        idb_type = getattr(model_mod, "IDesignBody")
        bodies_before = list(root.GetDescendants[idb_type]())
        
        try:
            ref = getattr(d_factory, "DirZ")
            if abs(direction.Z) > 0.9: ref = getattr(d_factory, "DirX")
            x_axis = getattr(d_factory, "Cross")(direction, ref)
            frame = getattr(getattr(geom_mod, "Frame"), "Create")(origin_pt, direction, x_axis)
            circle = getattr(getattr(geom_mod, "Circle"), "Create")(frame, MM(offset*1000))
            dc = getattr(getattr(model_mod, "DesignCurve"), "Create")(root, getattr(getattr(geom_mod, "CurveSegment"), "Create")(circle))
            
            getattr(getattr(cmd_mod, "ExtrudeEdges"), "Execute")(getattr(getattr(sel_mod, "Selection"), "Create")(dc.Edges[0]), origin_pt, direction, MM(10000), None, None)
            print("   [DEBUG 2] ExtrudeEdges success")
        except Exception as ce:
            print("   [DEBUG 2-FAIL] ExtrudeEdges failed: " + str(ce))
            return

        bodies_after = list(root.GetDescendants[idb_type]())
        new_b = next((b for b in bodies_after if b not in bodies_before), None)
        if new_b:
            print("   [DEBUG 3] Starting split")
            try: getattr(getattr(cmd_mod, "SplitBody"), "ByCutter")(getattr(getattr(sel_mod, "Selection"), "Create")(targets), getattr(getattr(sel_mod, "Selection"), "Create")(new_b.Faces[0]), True, None)
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
        p_factory = getattr(geom_mod, "Point")
        d_factory = getattr(geom_mod, "Direction")
        origin = getattr(p_factory, "Create")(MM(origin_list[0]*1000), MM(origin_list[1]*1000), MM(origin_list[2]*1000))
        normal = getattr(d_factory, "Create")(normal_list[0], normal_list[1], normal_list[2])
        
        doc = Window.ActiveWindow.Document
        root = doc.MainPart
        idb_type = getattr(model_mod, "IDesignBody")
        bodies_before = list(root.GetDescendants[idb_type]())
        
        try:
            ref = getattr(d_factory, "DirZ")
            if abs(normal.Z) > 0.9: ref = getattr(d_factory, "DirX")
            x_axis = getattr(d_factory, "Cross")(normal, ref)
            frame = getattr(getattr(geom_mod, "Frame"), "Create")(origin, normal, x_axis)
            circle = getattr(getattr(geom_mod, "Circle"), "Create")(frame, MM(20000)) 
            dc = getattr(getattr(model_mod, "DesignCurve"), "Create")(root, getattr(getattr(geom_mod, "CurveSegment"), "Create")(circle))
            
            try:
                getattr(getattr(cmd_mod, "Fill"), "Execute")(getattr(getattr(sel_mod, "Selection"), "Create")(dc.Edges[0]), None, None)
                print("   [DEBUG 3] Fill success")
            except:
                print("   [DEBUG 3-FAIL] Fill failed, trying DatumPlane")
                plane_obj = getattr(getattr(geom_mod, "Plane"), "Create")(frame)
                datum_plane = getattr(getattr(model_mod, "DatumPlane"), "Create")(root, "Cutter_Plane", plane_obj)
                getattr(getattr(cmd_mod, "SplitBody"), "ByCutter")(getattr(getattr(sel_mod, "Selection"), "Create")(targets), getattr(getattr(sel_mod, "Selection"), "Create")(datum_plane), True, None)
                _move_to_comp(datum_plane, b_idx)
                dc.Delete()
                return

            bodies_after = list(root.GetDescendants[idb_type]())
            new_b = next((b for b in bodies_after if b not in bodies_before), None)
            if new_b:
                print("   [DEBUG 4] Starting split")
                try: getattr(getattr(cmd_mod, "SplitBody"), "ByCutter")(getattr(getattr(sel_mod, "Selection"), "Create")(targets), getattr(getattr(sel_mod, "Selection"), "Create")(new_b.Faces[0]), True, None)
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
