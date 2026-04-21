import pandas as pd
import os
import math
from pathlib import Path

class APDLModelBuilder:
    def __init__(self, params_csv, extra_nodes_csv=None):
        self.params_df = pd.read_csv(params_csv)
        self.extra_nodes_csv = extra_nodes_csv
        self.node_map = {} # Name -> NodeID
        self.next_node_id = 1
        self.next_elem_id = 1
        self.next_mat_id = 1
        self.next_sec_id = 1
        self.next_real_id = 1
        self.apdl_lines = []

    def build(self, output_path):
        self.apdl_lines = []
        self._write_header()
        self._write_parameters()
        self._write_materials_and_types()
        self._write_sections()
        self._write_nodes_and_elements()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.apdl_lines))
        print(f"APDL model generated at {output_path}")

    def _write_header(self):
        self.apdl_lines.append("! Generated APDL Model for Reduced Order Analysis")
        self.apdl_lines.append("/PREP7")
        self.apdl_lines.append("FINISH\n/CLEAR\n/PREP7\n")

    def _write_parameters(self):
        self.apdl_lines.append("! --- Design Parameters (for Tuning) ---")
        for idx, row in self.params_df.iterrows():
            name = row['Name'].replace(" ", "_")
            if row['Type'] == "Cylinder":
                self.apdl_lines.append(f"VAR_{name}_OD = {row['OD_Avg']}")
                self.apdl_lines.append(f"VAR_{name}_ID = {row['ID_Avg']}")
            elif row['Type'] == "Plate":
                self.apdl_lines.append(f"VAR_{name}_TK = {row['Thickness']}")
                self.apdl_lines.append(f"VAR_{name}_OD = {row['OD_Avg']}")
        self.apdl_lines.append("")

    def _write_materials_and_types(self):
        self.apdl_lines.append("! --- Element Types and Materials ---")
        
        # Unique Material Property Groups (EX, PRXY, DENS)
        self.mat_map = {} # (EX, PRXY, DENS) -> MatID
        for idx, row in self.params_df.iterrows():
            # Get properties from CSV or use defaults
            ex = row.get('EX', 2.1e5)
            prxy = row.get('PRXY', 0.3)
            dens = row.get('Density', 7.85e-9) # Default to Ton/mm3
            
            prop_key = (ex, prxy, dens)
            if prop_key not in self.mat_map:
                mat_id = self.next_mat_id
                self.apdl_lines.append(f"MP,EX,{mat_id},{ex}")
                self.apdl_lines.append(f"MP,PRXY,{mat_id},{prxy}")
                self.apdl_lines.append(f"MP,DENS,{mat_id},{dens}")
                self.mat_map[prop_key] = mat_id
                self.next_mat_id += 1
        
        self.et_beam = 1
        self.et_shell = 2
        self.et_mass = 3
        self.apdl_lines.append(f"ET,{self.et_beam},188")
        self.apdl_lines.append(f"ET,{self.et_shell},181")
        self.apdl_lines.append(f"ET,{self.et_mass},21")
        self.apdl_lines.append(f"KEYOPT,{self.et_mass},3,0") # 3D mass with rot
        self.apdl_lines.append("")

    def _write_sections(self):
        self.apdl_lines.append("! --- Section Definitions ---")
        self.section_map = {}
        for idx, row in self.params_df.iterrows():
            name = row['Name'].replace(" ", "_")
            sec_id = self.next_sec_id
            self.section_map[name] = sec_id
            if row['Type'] == "Cylinder":
                self.apdl_lines.append(f"SECTYPE,{sec_id},PIPE,,{name}")
                self.apdl_lines.append(f"SECDATA,VAR_{name}_OD/2,VAR_{name}_ID/2")
            elif row['Type'] == "Plate":
                self.apdl_lines.append(f"SECTYPE,{sec_id},SHELL,,{name}")
                self.apdl_lines.append(f"SECDATA,VAR_{name}_TK,1")
            self.next_sec_id += 1
        self.apdl_lines.append("")

    def _write_nodes_and_elements(self):
        self.apdl_lines.append("! --- Nodes and Structural Elements ---")
        
        extra_nodes = []
        if self.extra_nodes_csv and os.path.exists(self.extra_nodes_csv):
            extra_nodes = pd.read_csv(self.extra_nodes_csv).to_dict('records')

        # Global Node Map (Z -> NodeID) to merge nodes at same Z
        self.global_z_nodes = {}

        def get_or_create_node(z, name=None):
            if z in self.global_z_nodes:
                nid = self.global_z_nodes[z]
                if name: self.node_map[name] = nid
                return nid
            else:
                nid = self.next_node_id
                self.apdl_lines.append(f"N,{nid},0,0,{z}")
                self.global_z_nodes[z] = nid
                if name: self.node_map[name] = nid
                self.next_node_id += 1
                return nid

        for idx, row in self.params_df.iterrows():
            name = row['Name'].replace(" ", "_")
            z_s = float(row.get('Z_Start', row['Z_Center'] - 50))
            z_e = float(row.get('Z_End', row['Z_Center'] + 50))
            z_cg = float(row['Z_Center'])
            
            # 1. Collect Backbone Z Points
            backbone_z_points = [z_s, z_e, z_cg]
            offset_nodes = []
            for en in extra_nodes:
                if z_s <= en['Z'] <= z_e:
                    if en.get('X', 0) == 0 and en.get('Y', 0) == 0:
                        backbone_z_points.append(en['Z'])
                    else:
                        offset_nodes.append(en)
            
            sorted_z = sorted(list(set(backbone_z_points)))
            
            # 2. Create Backbone Nodes
            section_backbone_nodes = []
            for z in sorted_z:
                node_alias = None
                if z == z_s: node_alias = f"{name}_Start"
                elif z == z_e: node_alias = f"{name}_End"
                elif z == z_cg: node_alias = f"{name}_CG"
                
                nid = get_or_create_node(z, node_alias)
                section_backbone_nodes.append(nid)
            
            # 3. Create Elements
            mat_id = self.mat_map[(row.get('EX', 2.1e5), row.get('PRXY', 0.3), row.get('Density', 7.85e-9))]
            sec_id = self.section_map[name]
            
            if row['Type'] == "Cylinder":
                self.apdl_lines.append(f"TYPE,{self.et_beam}")
                self.apdl_lines.append(f"MAT,{mat_id}")
                self.apdl_lines.append(f"SECNUM,{sec_id}")
                for i in range(len(section_backbone_nodes) - 1):
                    self.apdl_lines.append(f"E,{section_backbone_nodes[i]},{section_backbone_nodes[i+1]}")
                
                # Mass correction at CG
                self.apdl_lines.append(f"TYPE,{self.et_mass}")
                self.apdl_lines.append(f"MAT,{mat_id}")
                real_id = self.next_real_id
                self.apdl_lines.append(f"R,{real_id},{row['Mass']}, {row['Mass']}, {row['Mass']}, {row['Ixx']}, {row['Iyy']}, {row['Izz']}")
                self.apdl_lines.append(f"REAL,{real_id}")
                cg_node = self.node_map[f"{name}_CG"]
                self.apdl_lines.append(f"E,{cg_node}")
                self.next_real_id += 1

            elif row['Type'] == "Plate":
                self.apdl_lines.append(f"! --- Precision Shell Plate: {name} ---")
                backbone_node = self.node_map[f"{name}_CG"]
                radial_div = int(row.get('Radial_Divisions', 1)) # 기본 1분할
                
                # Create nodes at different radii
                rings = [] # List of lists of node IDs
                for r_idx in range(radial_div + 1):
                    current_r_ratio = r_idx / radial_div
                    ring_nodes = []
                    
                    if r_idx == 0:
                        # Center Node
                        nid = self.next_node_id
                        self.apdl_lines.append(f"N,{nid},0,0,{z_cg} ! {name}_Center")
                        ring_nodes.append(nid)
                        self.next_node_id += 1
                    else:
                        # Edge or Intermediate Ring (8 nodes each)
                        for i in range(8):
                            angle = i * (360/8)
                            nid = self.next_node_id
                            self.apdl_lines.append(f"N,{nid},VAR_{name}_OD/2*{current_r_ratio}*cos({angle}),VAR_{name}_OD/2*{current_r_ratio}*sin({angle}),{z_cg}")
                            ring_nodes.append(nid)
                            self.next_node_id += 1
                            
                            # If it's the outermost ring, connect to backbone via CERIG
                            if r_idx == radial_div:
                                self.apdl_lines.append(f"CERIG,{backbone_node},{nid},ALL")
                    
                    rings.append(ring_nodes)

                # Create Shell Elements between rings
                self.apdl_lines.append(f"TYPE,{self.et_shell}")
                self.apdl_lines.append(f"MAT,{mat_id}")
                self.apdl_lines.append(f"SECNUM,{sec_id}")
                
                for r_idx in range(radial_div):
                    inner_ring = rings[r_idx]
                    outer_ring = rings[r_idx+1]
                    
                    if r_idx == 0:
                        # Center to First Ring (Triangular elements)
                        center_nid = inner_ring[0]
                        for i in range(8):
                            self.apdl_lines.append(f"E,{center_nid},{outer_ring[i]},{outer_ring[(i+1)%8]}")
                    else:
                        # Ring to Ring (Quadrilateral elements)
                        for i in range(8):
                            self.apdl_lines.append(f"E,{inner_ring[i]},{inner_ring[(i+1)%8]},{outer_ring[(i+1)%8]},{outer_ring[i]}")
                
                # Mass correction at Center Node
                self.apdl_lines.append(f"TYPE,{self.et_mass}")
                real_id = self.next_real_id
                self.apdl_lines.append(f"R,{real_id},{row['Mass']}, {row['Mass']}, {row['Mass']}, {row['Ixx']}, {row['Iyy']}, {row['Izz']}")
                self.apdl_lines.append(f"REAL,{real_id}")
                self.apdl_lines.append(f"E,{rings[0][0]}")
                self.next_real_id += 1

            # 4. Handle Offset Nodes
            for on in offset_nodes:
                on_id = self.next_node_id
                self.apdl_lines.append(f"N,{on_id},{on['X']},{on['Y']},{on['Z']} ! {on['Name']}")
                self.node_map[on['Name']] = on_id
                self.next_node_id += 1
                anchor_node = get_or_create_node(on['Z'])
                self.apdl_lines.append(f"CERIG,{anchor_node},{on_id},ALL")

        self.apdl_lines.append("")

if __name__ == "__main__":
    # Test with materials
    dummy_csv = "test_params_final.csv"
    data = {
        'Name': ['Shaft_A', 'Disk_B'],
        'Type': ['Cylinder', 'Plate'],
        'Z_Center': [75.0, 160.0],
        'Z_Start': [0.0, 150.0],
        'Z_End': [150.0, 170.0],
        'Mass': [0.011775, 0.003925],
        'Density': [7.85e-9, 7.85e-9],
        'EX': [2.1e5, 2.1e5],
        'PRXY': [0.3, 0.3],
        'Thickness': [0, 20.0],
        'OD_Avg': [100.0, 300.0],
        'ID_Avg': [80.0, 0],
        'Ixx': [1000, 2000],
        'Iyy': [1000, 2000],
        'Izz': [500, 4000]
    }
    pd.DataFrame(data).to_csv(dummy_csv, index=False)
    
    builder = APDLModelBuilder(dummy_csv)
    builder.build("refined_model_v2.dat")
