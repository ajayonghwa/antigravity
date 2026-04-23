# -*- coding: utf-8 -*-
import os

class SCDMGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.output_dir = os.path.join(project_root, "04_scripts")
        if not os.path.exists(self.output_dir):
            try: os.makedirs(self.output_dir)
            except: self.output_dir = project_root

    def generate_script(self, plan_list, output_name="scdm_decomposition_script.py"):
        execution_calls = ""
        for i, plan in enumerate(plan_list):
            strat = plan.get("strategy", "").upper()
            body = plan.get("body_name", "Unknown")
            
            safe_body = body.replace("'", "\\'")
            
            if strat == "OGRID":
                execution_calls += f"apply_ogrid('{safe_body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {i})\n"
            elif strat == "CGRID":
                execution_calls += f"apply_cgrid('{safe_body}', {plan['center']}, {plan['axis']}, {plan['core_offset']}, {plan.get('wall_direction', [0,0,1])}, {i})\n"
            elif strat == "RADIAL_OFFSET":
                execution_calls += f"apply_radial_offset('{safe_body}', {plan['center']}, {plan['axis']}, {plan['split_radius']}, {i})\n"
            elif strat in ["AXIAL", "SECTOR", "HGRID", "YBLOCK_CUT"]:
                split = plan["split_plane"]
                execution_calls += f"apply_split_plane('{safe_body}', {split['origin']}, {split['normal']}, '{strat}', {i})\n"

        # [v4.21] SplitBody를 먼저 수행한 뒤에 커터를 컴포넌트로 이동시킵니다.
        # 서로 다른 컴포넌트에 있는 템플릿과 인스턴스 간의 불리언 연산은 스페이스클레임에서 실패하기 때문입니다.
        script_template = f"""# -*- coding: utf-8 -*-
import math

ALL_CUTTERS = []

def get_all_bodies_recursive(part, body_list):
    try:
        for b in part.GetDescendants[IDesignBody]():
            body_list.append(b)
        return
    except:
        pass
        
    for body in part.Bodies:
        body_list.append(body)
    for comp in part.Components:
        if hasattr(comp, "Content") and comp.Content:
            get_all_bodies_recursive(comp.Content, body_list)
        elif hasattr(comp, "Template") and comp.Template:
            get_all_bodies_recursive(comp.Template, body_list)

def get_matching_bodies(target_name):
    try:
        target_unicode = target_name.decode('utf-8')
    except:
        target_unicode = target_name
        
    all_bodies = []
    get_all_bodies_recursive(GetRootPart(), all_bodies)
    matched = []
    for b in all_bodies:
        if b.Name == target_unicode or b.Name.startswith(target_unicode + u"_"):
            matched.append(b)
    return matched

def _get_target_cutter_comp(target_body_name):
    root = GetRootPart()
    try: t_name = target_body_name.decode('utf-8')
    except: t_name = target_body_name
    
    safe_name = "".join(c for c in t_name if c.isalnum() or c == u"_")
    comp_name = "CUTTERS_FOR_" + safe_name
    
    for comp in root.Components:
        if comp.Name == comp_name: return comp
        
    try:
        new_part = Part.Create(root.Document, comp_name)
        new_comp = Component.Create(root, new_part)
        return new_comp
    except Exception as e:
        print("    [WARN] Failed to create component: " + str(e))
        return root

def _safe_split(target_body, cutter_face):
    try:
        res = SplitBody.ByCutter(Selection.Create(target_body), Selection.Create(cutter_face), True, None)
        if res.CreatedBodies.Count > 0: return True
    except: pass
    try:
        SplitBody.Execute(Selection.Create(target_body), Selection.Create(cutter_face))
        return True
    except: pass
    return False

def _create_cylindrical_cutter(target_body, origin_pt, direction, radius, name):
    try:
        root = GetRootPart()
        r = getattr(target_body.Shape, "Range", getattr(target_body, "Box", getattr(target_body, "BoundingBox", None)))
        extrude_dist = 2.0
        if r:
            diag = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2)
            extrude_dist = max(diag * 4.0, 0.1)
        
        shifted_origin = Point.Create(origin_pt.X - direction.X * extrude_dist/2, 
                                      origin_pt.Y - direction.Y * extrude_dist/2, 
                                      origin_pt.Z - direction.Z * extrude_dist/2)
        
        frame = Frame.Create(shifted_origin, direction)
        circle = Circle.Create(frame, radius)
        design_curve = DesignCurve.Create(root, CurveSegment.Create(circle))
        
        sel = Selection.Create(design_curve)
        try: ExtrudeEdges.Execute(sel, extrude_dist, ExtrudeEdgeOptions(), None)
        except: 
            try: ExtrudeEdges.Execute(sel, Selection.Create(direction), extrude_dist, ExtrudeEdgeOptions(), None)
            except: pass
        
        tool = None
        for b in root.Bodies:
            if getattr(b, 'Shape', None) and "Cylinder" in b.Shape.Geometry.GetType().Name:
                if b.Name.startswith("Solid") or b.Name.startswith("솔리드"):
                    tool = b
                    
        if not tool and root.Bodies.Count > 0:
            tool = root.Bodies[-1]
            
        design_curve.Delete()
        
        if tool:
            tool.Name = name
            # [v4.21] 여기서는 생성만 하고 이동은 Split 이후에 하도록 부모 변경을 삭제함.
            return tool
        return None
    except: return None

def apply_ogrid(target_name, center, axis, offset, idx):
    global ALL_CUTTERS
    try: print(" -> Step {{0}}: O-GRID for {{1}}".format(idx, target_name.decode('utf-8')))
    except: print(" -> Step {{0}}: O-GRID".format(idx))
        
    targets = get_matching_bodies(target_name)
    if not targets:
        print("    [ERROR] Could not find target body")
        return

    origin_pt = Point.Create(center[0], center[1], center[2])
    direction = Direction.Create(axis[0], axis[1], axis[2])

    for i, target in enumerate(targets):
        cutter_name = "Cutter_OGrid_Hole_{{0}}_{{1}}".format(idx, i)
        tool = _create_cylindrical_cutter(target, origin_pt, direction, offset, cutter_name)
        if tool:
            ALL_CUTTERS.append(tool)
            cutter_face = None
            for face in tool.Faces:
                if "Cylinder" in face.Shape.Geometry.GetType().Name:
                    cutter_face = face
                    break
            if not cutter_face: cutter_face = tool.Faces[0]
            
            # [v4.21] 커터가 루트(동일 컨텍스트)에 있을 때 먼저 자릅니다!
            if _safe_split(target, cutter_face):
                print("    [OK] Split Success")
            else:
                print("    [FAIL] Split failed")
                
            # 자르기가 끝난 뒤에 비로소 컴포넌트로 치웁니다.
            try:
                parent_comp = _get_target_cutter_comp(target.Name)
                tool.SetParent(parent_comp)
            except: pass

def apply_split_plane(target_name, origin_list, normal_list, strategy, idx):
    global ALL_CUTTERS
    try: print(" -> Step {{0}}: {{1}} for {{2}}".format(idx, strategy, target_name.decode('utf-8')))
    except: print(" -> Step {{0}}: {{1}}".format(idx, strategy))
    
    targets = get_matching_bodies(target_name)
    if not targets:
        print("    [ERROR] Could not find target body")
        return
    
    origin = Point.Create(origin_list[0], origin_list[1], origin_list[2])
    normal = Direction.Create(normal_list[0], normal_list[1], normal_list[2])
    frame = Frame.Create(origin, normal)
    root = GetRootPart()

    for i, target in enumerate(targets):
        try:
            r = getattr(target.Shape, "Range", getattr(target, "Box", getattr(target, "BoundingBox", None)))
            huge_radius = 5.0
            if r:
                huge_radius = math.sqrt((r.Max.X - r.Min.X)**2 + (r.Max.Y - r.Min.Y)**2 + (r.Max.Z - r.Min.Z)**2) * 4.0
            
            circle_geom = Circle.Create(frame, huge_radius)
            design_curve = DesignCurve.Create(root, CurveSegment.Create(circle_geom))
            
            Fill.Execute(Selection.Create(design_curve))
            
            tool = None
            for b in root.Bodies:
                if getattr(b, 'Shape', None) and "Plane" in b.Shape.Geometry.GetType().Name:
                    if b.Name.startswith("Surface") or b.Name.startswith("서피스"):
                        tool = b
            if not tool and root.Bodies.Count > 0:
                tool = root.Bodies[-1]
            
            if tool:
                tool.Name = "Cutter_{{0}}_{{1}}_{{2}}".format(strategy, idx, i)
                ALL_CUTTERS.append(tool)
                
                # [v4.21] 커터가 루트(동일 컨텍스트)에 있을 때 먼저 자릅니다!
                if _safe_split(target, tool.Faces[0]):
                    print("    [OK] Split Success")
                else:
                    print("    [FAIL] Split failed")
                    
                # 자르기가 끝난 뒤에 비로소 컴포넌트로 치웁니다.
                try:
                    parent_comp = _get_target_cutter_comp(target.Name)
                    tool.SetParent(parent_comp)
                except: pass
                
            design_curve.Delete()
        except: pass

def finalize():
    print(" --- Finished ---")

# --- EXECUTION ---
{execution_calls}
finalize()
"""
        output_path = os.path.join(self.output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_template)
        return output_path
