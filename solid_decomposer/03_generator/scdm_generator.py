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
                if not center: 
                    print(f"   [WARN] No center for {strat} on {body}")
                    continue
                center_m = [c * scale for c in center]
                axis = plan.get('axis', [0,0,1])
                offset_m = plan.get('core_offset', 1.0) * scale
                
                if strat == "OGRID":
                    execution_calls += "apply_ogrid('{0}', {1}, {2}, {3}, {4}, {5})\n".format(body_b64, center_m, axis, offset_m, i, body_idx)
                elif strat == "CGRID":
                    wall_dir = plan.get('wall_direction', [0,0,1])
                    execution_calls += "apply_cgrid('{0}', {1}, {2}, {3}, {4}, {5}, {6})\n".format(body_b64, center_m, axis, offset_m, wall_dir, i, body_idx)
                elif strat == "RADIAL_OFFSET":
                    r_m = plan.get('split_radius', 1.0) * scale
                    execution_calls += "apply_radial_offset('{0}', {1}, {2}, {3}, {4}, {5})\n".format(body_b64, center_m, axis, r_m, i, body_idx)
            
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan.get("split_plane")
                if not split: 
                    print(f"   [WARN] No split_plane for {strat} on {body}")
                    continue
                origin_m = [o * scale for o in split['origin']]
                normal = split.get('normal', [0,0,1])
                execution_calls += "apply_split_plane('{0}', {1}, {2}, '{3}', {4}, {5})\n".format(body_b64, origin_m, normal, strat, i, body_idx)

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
    try: target_name = base64.b64decode(body_b64).decode('utf-8')
    except: target_name = body_b64
    all_bodies = []
    root = GetRootPart()
    try:
        desc = list(root.GetDescendants[IDesignBody]())
        for b in desc: all_bodies.append(b)
        if not desc:
            for b in root.Bodies: all_bodies.append(b)
    except: pass
    
    matched = []
    pattern = re.compile(re.escape(target_name) + r"(_|\\s|\\(|\\d|$)")
    for b in all_bodies:
        if pattern.match(b.Name): matched.append(b)
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

def _move_to_comp(body, body_idx):
    target_comp = BODY_COMP_MAP.get(body_idx)
    if not target_comp: return
    try: ComponentHelper.MoveBodiesToComponent(Selection.Create(body), target_comp)
    except: pass

def apply_ogrid(body_b64, center, axis, offset, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])
    root = GetRootPart()
    try:
        bodies_before = list(root.GetDescendants[IDesignBody]())
        circle = Circle.Create(Frame.Create(origin_pt, direction), offset)
        dc = DesignCurve.Create(root, CurveSegment.Create(circle))
        try: ExtrudeEdges.Execute(Selection.Create(dc), 0.2, ExtrudeEdgeOptions(), None)
        except: pass
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_b = [b for b in bodies_after if b not in bodies_before]
        if new_b:
            SplitBody.ByCutter(Selection.Create(targets), Selection.Create(new_b[0].Faces[0]), True, None)
            _move_to_comp(new_b[0], b_idx)
        dc.Delete()
    except: pass

def apply_split_plane(body_b64, origin_list, normal_list, strategy, idx, b_idx):
    targets = get_matching_bodies(body_b64)
    if not targets: return
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    root = GetRootPart()
    try:
        bodies_before = list(root.GetDescendants[IDesignBody]())
        circle = Circle.Create(Frame.Create(origin, normal), 1.0) # 임시 반경
        dc = DesignCurve.Create(root, CurveSegment.Create(circle))
        try: Fill.Execute(Selection.Create(dc), None, FillOptions(), None)
        except: pass
        bodies_after = list(root.GetDescendants[IDesignBody]())
        new_b = [b for b in bodies_after if b not in bodies_before]
        if new_b:
            SplitBody.ByCutter(Selection.Create(targets), Selection.Create(new_b[0].Faces[0]), True, None)
            _move_to_comp(new_b[0], b_idx)
        dc.Delete()
    except: pass

REPLACE_COMP_CREATION
REPLACE_EXECUTION
print("Decomposition Finished.")
"""
        script_content = template.replace("REPLACE_COMP_CREATION", comp_creation_calls)
        script_content = script_content.replace("REPLACE_EXECUTION", execution_calls)
        
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w") as f: f.write(script_content)
        return output_path
