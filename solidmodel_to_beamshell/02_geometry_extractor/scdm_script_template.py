# SpaceClaim IronPython Script for Geometry Extraction
# This script is intended to be run INSIDE SpaceClaim (IronPython environment)

import os

# --- Helper Functions ---
def get_cylinder_properties(body):
    """Calculate min/max/avg ID and OD for a cylindrical body."""
    radii = []
    for face in body.Faces:
        # Check if the face is cylindrical
        if str(face.Shape.Type) == 'Cylinder':
            radii.append(face.Shape.Radius)
    
    if not radii:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    
    radii.sort()
    # Assuming the larger radii are OD and smaller are ID
    # In a simple tube, we'd have two unique radii. 
    # For PoC, we take the max as OD and min as ID.
    od_list = [r for r in radii if r > sum(radii)/len(radii)]
    id_list = [r for r in radii if r <= sum(radii)/len(radii)]
    
    od_avg = sum(od_list)/len(od_list) if od_list else max(radii)
    id_avg = sum(id_list)/len(id_list) if id_list else 0.0
    
    return od_avg, min(od_list) if od_list else od_avg, max(od_list) if od_list else od_avg, \
           id_avg, min(id_list) if id_list else id_avg, max(id_list) if id_list else id_avg

def get_plate_properties(body):
    """Calculate OD and Thickness for a plate."""
    # Thickness can be estimated from the Bounding Box Z-extent
    bbox = body.GetBoundingBox(Matrix.Identity)
    thickness = bbox.High.Z - bbox.Low.Z
    
    # OD can be estimated from X or Y extent
    od = max(bbox.High.X - bbox.Low.X, bbox.High.Y - bbox.Low.Y)
    return od, thickness

# --- Main Script Execution ---
geometry_path = r"{GEOMETRY_PATH}"
output_path = r"{OUTPUT_PATH}"
sections = {SECTIONS}

# 0. Set Units to mm (Force: N, Length: mm)
# 이 코드는 SCDM의 세션 단위를 mm로 강제 고정합니다.
options = LoadFileOptions.Create()
DocumentHelper.Open(geometry_path, options)

# SCDM API를 이용한 단위계 설정
# 버전/환경에 따라 아래 방식 중 하나가 작동합니다.
try:
    # 2024 R1 방식
    Session.Units.Length.SetUnits(UnitType.Millimeters)
except:
    # 구형 방식 대응 (주석 처리로 남겨둠)
    # MM = UnitType.Millimeters
    pass

results = []
results.append("Name,Type,Z_Center,Volume,MassCenter_Z,Ixx,Iyy,Izz,OD_Avg,OD_Min,OD_Max,ID_Avg,ID_Min,ID_Max,Thickness")

for sec in sections:
    name = sec['name']
    z_start = sec['z_start']
    z_end = sec['z_end']
    s_type = sec['type']
    
    # 1. Create Planes and Split
    # (Simplified for PoC: This assumes a single main body exists)
    # In real usage, we iterate over all bodies in the Part
    target_bodies = list(Window.ActiveWindow.Scene.GetRootPart().AllBodies)
    
    # Create splitting planes at Z positions
    plane_start = DatumPlaneCreator.Create(Point.Create(0, 0, z_start), Direction.DirZ)
    plane_end = DatumPlaneCreator.Create(Point.Create(0, 0, z_end), Direction.DirZ)
    
    # This is a simplified split logic. In SCDM API, Combine.SplitBody is used.
    # Note: For the actual implementation, we might need to handle body selection carefully.
    
    # 2. Extract Data from the body between Z_start and Z_end
    # For PoC, let's assume we can identify the resulting body by its center
    extracted_body = None
    for body in Window.ActiveWindow.Scene.GetRootPart().AllBodies:
        bbox = body.GetBoundingBox(Matrix.Identity)
        z_center = (bbox.High.Z + bbox.Low.Z) / 2.0
        if z_start < z_center < z_end:
            extracted_body = body
            break
            
    if extracted_body:
        props = extracted_body.GetMassProperties()
        vol = props.Volume
        cg_z = props.MassCenter.Z
        # Moments are relative to CG
        ixx = props.PrincipalMoments.X
        iyy = props.PrincipalMoments.Y
        izz = props.PrincipalMoments.Z
        
        od_avg, od_min, od_max, id_avg, id_min, id_max = (0,0,0,0,0,0)
        thickness = 0
        
        if s_type == "Cylinder":
            od_avg, od_min, od_max, id_avg, id_min, id_max = get_cylinder_properties(extracted_body)
        elif s_type == "Plate":
            od_avg, thickness = get_plate_properties(extracted_body)
            
        line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}".format(
            name, s_type, cg_z, vol, cg_z, ixx, iyy, izz, od_avg, od_min, od_max, id_avg, id_min, id_max, thickness
        )
        results.append(line)

# Write to CSV
with open(output_path, "w") as f:
    f.write("\n".join(results))

# Close without saving
DocumentHelper.Close()
