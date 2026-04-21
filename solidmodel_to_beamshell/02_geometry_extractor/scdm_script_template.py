# -*- coding: utf-8 -*-
# Upgraded SpaceClaim IronPython Script for Geometry Extraction
# Optimized for: Representative Beam/Shell Property Extraction (with Min/Max Ranges)

import os
import math

class SafeSCDM:
    @staticmethod
    def split_and_get_middle(body, z_pos, is_upper=True):
        plane = Plane.Create(Frame.Create(Point.Create(0,0,z_pos), Vector.Create(0,0,1)))
        res = SplitBody.ByCutter(Selection.Create(body), plane)
        if not res or not res.Success or res.CreatedBodies.Count < 2:
            return body
            
        all_pieces = [cb for cb in res.CreatedBodies]
        sorted_pieces = sorted(all_pieces, key=lambda b: b.GetBoundingBox(Matrix.Identity).Center.Z)
        return sorted_pieces[-1] if is_upper else sorted_pieces[0]

def get_cylinder_properties(body):
    """지배적인 내외경의 평균(Avg)과 변동 범위(Min, Max)를 모두 추출"""
    ext_radii = []
    int_radii = []
    
    for face in body.Faces:
        if str(face.Shape.Type) == 'Cylinder':
            r = face.Shape.Radius
            normal = face.NormalAt(Parameter.Create(0.5, 0.5))
            center = face.Box.Center
            radial = Vector.Create(center.X, center.Y, 0).Direction
            is_internal = Vector.Dot(radial, normal) < -0.1
            
            if is_internal:
                int_radii.append(r)
            else:
                ext_radii.append(r)
                
    def get_stats(radii):
        if not radii: return 0, 0, 0
        avg = sum(radii) / len(radii)
        return avg, min(radii), max(radii)

    od_avg, od_min, od_max = get_stats(ext_radii)
    id_avg, id_min, id_max = get_stats(int_radii)
    return od_avg, od_min, od_max, id_avg, id_min, id_max

def get_plate_properties(body):
    z_faces = []
    for face in body.Faces:
        if str(face.Shape.Type) == 'Plane':
            norm = face.NormalAt(Parameter.Create(0.5, 0.5))
            if abs(norm.Z) > 0.9:
                z_faces.append(face)
    
    if len(z_faces) < 2: return 0, 0
    z_faces.sort(key=lambda f: f.Area, reverse=True)
    f1 = z_faces[0]
    f2 = z_faces[1]
    
    thickness = abs(f1.Box.Center.Z - f2.Box.Center.Z)
    od = max(body.Box.Size.X, body.Box.Size.Y)
    return od, thickness

# --- Main Script Execution ---
geometry_path = r"{GEOMETRY_PATH}"
output_path = r"{OUTPUT_PATH}"
sections = {SECTIONS}

DocumentHelper.Open(geometry_path)
try: Session.Units.Length.SetUnits(UnitType.Millimeters)
except: pass

results = []
# 헤더에 Min, Max 추가
header = "Name,Type,Z_Center,Volume,Ixx,Iyy,Izz,OD_Avg,OD_Min,OD_Max,ID_Avg,ID_Min,ID_Max,Thickness"
results.append(header)

root = GetRootPart()
main_body = root.AllBodies[0]

for sec in sections:
    temp_body = main_body.Copy().CreatedBodies[0]
    slice_top = SafeSCDM.split_and_get_middle(temp_body, sec['z_start'], is_upper=True)
    final_slice = SafeSCDM.split_and_get_middle(slice_top, sec['z_end'], is_upper=False)
    
    props = final_slice.GetMassProperties()
    od_avg, od_min, od_max, id_avg, id_min, id_max = 0, 0, 0, 0, 0, 0
    thick = 0
    
    if sec['type'] == "Cylinder":
        od_avg, od_min, od_max, id_avg, id_min, id_max = get_cylinder_properties(final_slice)
    elif sec['type'] == "Plate":
        od_avg, thick = get_plate_properties(final_slice)
        od_min, od_max = od_avg, od_avg
        
    line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}".format(
        sec['name'], sec['type'], props.MassCenter.Z, props.Volume,
        props.PrincipalMoments.X, props.PrincipalMoments.Y, props.PrincipalMoments.Z,
        od_avg, od_min, od_max, id_avg, id_min, id_max, thick
    )
    results.append(line)
    final_slice.Delete()

with open(output_path, "w") as f:
    f.write("\n".join(results))

DocumentHelper.Close()
