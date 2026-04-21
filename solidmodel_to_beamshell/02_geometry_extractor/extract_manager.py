import json
import os
import subprocess
import csv
from pathlib import Path

class GeometryExtractManager:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.scdm_path = self.config.get('scdm_path', r"C:\Program Files\ANSYS Inc\v241\scdm\SpaceClaim.exe")
        self.template_path = Path(__file__).parent / "scdm_script_template.py"

    def generate_scdm_script(self):
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        sections_str = json.dumps(self.config['sections'])
        geometry_path = self.config['geometry_file'].replace("\\", "\\\\")
        output_csv = os.path.join(self.config['output_dir'], "raw_data.csv").replace("\\", "\\\\")
        
        script_content = template.replace("{GEOMETRY_PATH}", geometry_path)
        script_content = script_content.replace("{OUTPUT_PATH}", output_csv)
        script_content = script_content.replace("{SECTIONS}", sections_str)
        
        temp_script = Path(self.config['output_dir']) / "run_extract.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return temp_script

    def run_spaceclaim(self, script_path):
        print(f"Starting SpaceClaim at {self.scdm_path}...")
        cmd = [self.scdm_path, f"/RunScript={script_path}", "/Headless"]
        try:
            subprocess.run(cmd, check=True)
            print("SpaceClaim script execution finished.")
        except Exception as e:
            print(f"Error running SpaceClaim: {e}")

    def refine_data(self):
        """raw_data.csv를 읽어 튜닝 범위를 포함한 final_parameters.csv 생성"""
        raw_csv = Path(self.config['output_dir']) / "raw_data.csv"
        final_csv = Path(self.config['output_dir']) / "final_parameters.csv"
        
        if not raw_csv.exists():
            print(f"Error: raw_data.csv not found at {raw_csv}")
            return

        refined_results = []
        with open(raw_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Name']
                conf = next((s for s in self.config['sections'] if s['name'] == name), {})
                
                density = conf.get('density', 7.85e-9) # Default to Ton/mm3
                margin = conf.get('tuning_margin', 0.2)
                
                volume = float(row['Volume'])
                mass = volume * density
                row['Mass'] = mass
                row['Density'] = density
                
                # 튜닝 범위 계산 (물리적 Min/Max + 사용자 Margin)
                if row['Type'] == "Cylinder":
                    row['OD_Tuning_Min'] = float(row['OD_Min']) * (1 - margin)
                    row['OD_Tuning_Max'] = float(row['OD_Max']) * (1 + margin)
                    row['ID_Tuning_Min'] = float(row['ID_Min']) * (1 - margin)
                    row['ID_Tuning_Max'] = float(row['ID_Max']) * (1 + margin)
                elif row['Type'] == "Plate":
                    row['Thk_Tuning_Min'] = float(row['Thickness']) * (1 - margin)
                    row['Thk_Tuning_Max'] = float(row['Thickness']) * (1 + margin)
                
                refined_results.append(row)

        if refined_results:
            all_keys = set()
            for res in refined_results:
                all_keys.update(res.keys())
            
            base_keys = ["Name", "Type", "Z_Center", "Mass", "Density", "Volume"]
            sorted_keys = [k for k in base_keys if k in all_keys]
            sorted_keys += sorted([k for k in all_keys if k not in base_keys])

            with open(final_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=sorted_keys)
                writer.writeheader()
                writer.writerows(refined_results)
            print(f"Final parameters saved to {final_csv}")

if __name__ == "__main__":
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "sample_config.json"
    manager = GeometryExtractManager(config_file)
    script = manager.generate_scdm_script()
    # manager.run_spaceclaim(script)
    # manager.refine_data()
