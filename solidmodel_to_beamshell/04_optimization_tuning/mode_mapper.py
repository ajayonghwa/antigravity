import pandas as pd
import numpy as np
import json
from ansys.dpf import core as dpf

class ModeMapper:
    def __init__(self, rst_path, params_csv):
        self.rst_path = rst_path
        self.params_df = pd.read_csv(params_csv)
        self.model = dpf.Model(rst_path)
        self.mesh = self.model.metadata.meshed_region
        self.nodes = self.mesh.nodes

    def extract_mapped_modes(self, mode_indices, z_tol=1.0, r_margin=0.05):
        """
        Extract 3D mode shapes and map them to reduced model coordinates.
        mode_indices: List of mode numbers to extract (e.g., [1, 2, 5])
        z_tol: Tolerance for Z-coordinate matching (mm)
        r_margin: Percentage margin for outer radius selection (e.g., 0.05 for 95%~100%)
        """
        results = {}

        # 1. Get Displacements for specified modes
        # Note: DPF indices are often 0-based or use a field container
        disp_op = self.model.results.displacement()
        disp_op.inputs.time_scoping.connect(mode_indices)
        fields_container = disp_op.outputs.fields_container()

        # 2. Iterate through sections to find matching 3D nodes
        for idx, row in self.params_df.iterrows():
            sec_name = row['Name']
            z_target = float(row['Z_Center'])
            r_outer = float(row['OD_Avg']) / 2.0
            
            # Find nodes at Z_target +/- z_tol
            coords = self.nodes.coordinates_field.data
            all_ids = self.nodes.scoping.ids
            
            # Map of RadiusRatio -> List of NodeIDs
            # Example: {0.0: [nid1], 0.5: [nid2, nid3...], 1.0: [nid4...]}
            radial_nodes_map = {}
            radial_div = int(row.get('Radial_Divisions', 1))
            target_r_ratios = [i/radial_div for i in range(radial_div + 1)]
            for r_ratio in target_r_ratios:
                radial_nodes_map[r_ratio] = []

            for i, coord in enumerate(coords):
                x, y, z = coord
                if abs(z - z_target) <= z_tol:
                    radius = np.sqrt(x**2 + y**2)
                    
                    if row['Type'] == "Cylinder":
                        if r_outer * (1 - r_margin) <= radius <= r_outer * (1 + r_margin):
                            radial_nodes_map[1.0].append(all_ids[i])
                    elif row['Type'] == "Plate":
                        # Find which radial ring this node belongs to
                        current_ratio = radius / r_outer
                        for r_ratio in target_r_ratios:
                            # Using a 10% tolerance for radial matching
                            if abs(current_ratio - r_ratio) <= 0.1:
                                radial_nodes_map[r_ratio].append(all_ids[i])
                                break
            
            # 3. Average results for these radial groups across all modes
            sec_results = []
            for mode_idx in mode_indices:
                field = fields_container.get_field_by_time_id(mode_idx)
                
                # Dictionary to store averaged [UX, UY, UZ] per radius ratio
                averaged_radial_disp = {}
                for r_ratio, nids in radial_nodes_map.items():
                    if nids:
                        sub_field = field.get_entity_data_by_id(nids)
                        avg_disp = np.mean(sub_field, axis=0)
                        averaged_radial_disp[str(r_ratio)] = avg_disp.tolist()
                    else:
                        averaged_radial_disp[str(r_ratio)] = [0.0, 0.0, 0.0]
                
                freq = self.model.metadata.time_freq_support.get_frequency(step_index=0, cumulative_index=mode_idx-1)
                
                sec_results.append({
                    "mode_index": mode_idx,
                    "freq": float(freq),
                    "radial_displacements": averaged_radial_disp # { "0.0": [...], "1.0": [...] }
                })
            
            results[sec_name] = sec_results

        return results

    def save_reference(self, results, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Mapped 3D mode data saved to {output_path}")

if __name__ == "__main__":
    # Example usage:
    # mapper = ModeMapper("path/to/result.rst", "final_parameters.csv")
    # target_modes = [1, 2, 3, 5, 8] # Modes selected by user
    # data = mapper.extract_mapped_modes(target_modes)
    # mapper.save_reference(data, "reference_modes.json")
    print("ModeMapper script created. DPF usage requires a valid .rst file.")
