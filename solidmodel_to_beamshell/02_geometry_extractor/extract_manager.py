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
        """Fill the template with actual data from config."""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Prepare data for replacement
        sections_str = json.dumps(self.config['sections'])
        geometry_path = self.config['geometry_file'].replace("\\", "\\\\")
        output_csv = os.path.join(self.config['output_dir'], "raw_data.csv").replace("\\", "\\\\")
        
        # Replace placeholders
        script_content = template.replace("{GEOMETRY_PATH}", geometry_path)
        script_content = script_content.replace("{OUTPUT_PATH}", output_csv)
        script_content = script_content.replace("{SECTIONS}", sections_str)
        
        temp_script = Path(self.config['output_dir']) / "run_extract.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return temp_script

    def run_spaceclaim(self, script_path):
        """Execute SpaceClaim in batch mode with the generated script."""
        print(f"Starting SpaceClaim at {self.scdm_path}...")
        # Command line arguments for SpaceClaim
        # /RunScript: executes a script and then exits (usually)
        # /Headless: runs without UI
        cmd = [self.scdm_path, f"/RunScript={script_path}", "/Headless"]
        
        try:
            # Note: In a real Windows environment, shell=True or specific path handling might be needed
            subprocess.run(cmd, check=True)
            print("SpaceClaim script execution finished.")
        except Exception as e:
            print(f"Error running SpaceClaim: {e}")

    def refine_data(self):
        """Read raw_data.csv and add tuning margins and mass calculation."""
        raw_csv = Path(self.config['output_dir']) / "raw_data.csv"
        final_csv = Path(self.config['output_dir']) / "final_parameters.csv"
        
        if not raw_csv.exists():
            print(f"Error: raw_data.csv not found at {raw_csv}")
            return

        refined_results = []
        with open(raw_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Find matching config for density and margin
                name = row['Name']
                conf = next((s for s in self.config['sections'] if s['name'] == name), {})
                
                density = conf.get('density', 7850.0)
                margin = conf.get('tuning_margin', 0.2)
                
                # Calculate Mass: Volume (mm^3) * Density (kg/m^3) * 1e-9 = kg
                volume = float(row['Volume'])
                mass = volume * density * 1e-9
                row['Mass'] = mass
                row['Density'] = density
                
                # Add Tuning Ranges
                # For Cylinders
                if row['Type'] == "Cylinder":
                    row['OD_Tuning_Min'] = float(row['OD_Min']) * (1 - margin)
                    row['OD_Tuning_Max'] = float(row['OD_Max']) * (1 + margin)
                    row['ID_Tuning_Min'] = float(row['ID_Min']) * (1 - margin)
                    row['ID_Tuning_Max'] = float(row['ID_Max']) * (1 + margin)
                
                # For Plates
                elif row['Type'] == "Plate":
                    row['Thk_Tuning_Min'] = float(row['Thickness']) * (1 - margin)
                    row['Thk_Tuning_Max'] = float(row['Thickness']) * (1 + margin)
                
                refined_results.append(row)

        # Write final CSV
        if refined_results:
            # 모든 결과 행에서 사용된 모든 키를 수집하여 헤더를 만듭니다.
            all_keys = set()
            for res in refined_results:
                all_keys.update(res.keys())
            
            # 보기 좋게 정렬 (순서는 유지하되 추가된 키들은 뒤로)
            base_keys = ["Name", "Type", "Z_Center", "Mass", "Density", "Volume"]
            sorted_keys = [k for k in base_keys if k in all_keys]
            sorted_keys += sorted([k for k in all_keys if k not in base_keys])

            with open(final_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=sorted_keys)
                writer.writeheader()
                writer.writerows(refined_results)
            print(f"Final parameters saved to {final_csv}")

if __name__ == "__main__":
    # In Windows, user would run: python extract_manager.py sample_config.json
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "sample_config.json"
    
    manager = GeometryExtractManager(config_file)
    # 1. Generate script
    script = manager.generate_scdm_script()
    # 2. Run SpaceClaim (This will fail in this Mac environment, but is ready for Windows)
    # manager.run_spaceclaim(script)
    # 3. Refine (Assuming raw_data.csv exists for demonstration)
    # manager.refine_data()
