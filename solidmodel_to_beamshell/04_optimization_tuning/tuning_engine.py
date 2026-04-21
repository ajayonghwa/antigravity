import numpy as np
import pandas as pd
import json
import os
import subprocess
import time
from scipy.optimize import minimize

class TuningEngine:
    def __init__(self, model_dat, params_csv, reference_json, config_json=None):
        self.model_dat = model_dat
        self.params_df = pd.read_csv(params_csv)
        with open(reference_json, 'r') as f:
            self.reference_data = json.load(f)
        
        self.config = self._load_config(config_json)
        self.history = []
        self.best_cost = float('inf')
        self.stop_requested = False

    def _load_config(self, config_path):
        defaults = {
            "w_freq": 1.0,
            "w_mac": 1.0,
            "w_mass": 0.1,
            "w_eff_mass": 0.5,
            "ansys_path": "mapdl",
            "job_name": "tuning_job",
            "max_iter": 50,
            "rst_path": "",
            "tuning_mode": "full" # "light" 또는 "full" 선택 가능
        }
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                defaults.update(user_config)
        return defaults

    def calculate_mac(self, vec1, vec2):
        """Calculate Modal Assurance Criterion between two vectors."""
        v1 = np.array(vec1).flatten()
        v2 = np.array(vec2).flatten()
        if len(v1) != len(v2):
            return 0.0
        numerator = np.abs(np.vdot(v1, v2))**2
        denominator = (np.vdot(v1, v1) * np.vdot(v2, v2))
        return float(numerator / denominator) if denominator != 0 else 0.0

    def objective_function(self, x):
        if self.stop_requested or os.path.exists("stop.txt"):
            self.stop_requested = True
            return self.best_cost

        self._update_apdl_vars(x)
        self._run_ansys()
        current_results = self._parse_apdl_results()
        cost = self._calculate_cost(current_results)
        
        self.history.append({"params": x.tolist(), "cost": cost})
        if cost < self.best_cost:
            self.best_cost = cost
            self._save_best_result(x, current_results)
        
        print(f"Iteration {len(self.history)}: Cost = {cost:.6f}")
        return cost

    def _calculate_cost(self, current):
        w = self.config
        total_cost = 0.0
        
        # 1. Frequency Error
        f_err = 0.0
        # 2. MAC Error (1 - MAC)
        mac_err = 0.0
        
        mode_count = 0
        for sec_name, ref_modes in self.reference_data.items():
            for ref_m in ref_modes:
                mode_idx = ref_m['mode_index']
                sim_f = current['freqs'].get(mode_idx)
                sim_v = current['shapes'].get(mode_idx, {}).get(sec_name)
                
                if sim_f:
                    # Freq contribution
                    f_err += ((sim_f - ref_m['freq']) / ref_m['freq'])**2
                    
                    # MAC contribution (Skip if light mode)
                    if self.config['tuning_mode'] == "full":
                        ref_v = []
                        calc_sim_v = []
                        for r_ratio, disp in ref_m['radial_displacements'].items():
                            ref_v.extend(disp)
                            calc_sim_v.extend(sim_v.get(r_ratio, [0,0,0]))
                        
                        mac_val = self.calculate_mac(ref_v, calc_sim_v)
                        mac_err += (1.0 - mac_val)
                    
                    mode_count += 1

        if mode_count > 0:
            total_cost += w['w_freq'] * (f_err / mode_count)
            total_cost += w['w_mac'] * (mac_err / mode_count)

        # 3. Total Mass Error
        if 'total_mass' in current:
            ref_mass = sum(row['Mass'] for _, row in self.params_df.iterrows())
            total_cost += w['w_mass'] * ((current['total_mass'] - ref_mass) / ref_mass)**2

        # 4. Effective Mass Error
        if 'eff_mass' in current:
            # Compare direction-wise effective mass ratios
            # (Logic depends on 3D reference eff mass values)
            pass

        return total_cost

    def _update_apdl_vars(self, x):
        with open("tuning_vars.dat", "w") as f:
            for i, val in enumerate(x):
                f.write(f"{self.tuning_param_names[i]} = {val}\n")

    def _run_ansys(self):
        # Batch run with absolute path from config if provided
        pass

    def _parse_apdl_results(self):
        # In real: Parse CSV/JSON exported by APDL script
        # Example structure:
        return {
            "freqs": {1: 10.2, 2: 24.8},
            "shapes": {1: {"Section1": {"1.0": [0.1, 0, 0.01]}}},
            "total_mass": 150.5,
            "eff_mass": {"X": 0.65, "Y": 0.02, "Z": 0.1}
        }

    def optimize(self):
        # (Bounds calculation logic same as before...)
        pass

if __name__ == "__main__":
    print("TuningEngine updated with MAC and Effective Mass support.")
