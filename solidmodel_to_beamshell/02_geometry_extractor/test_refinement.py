import csv
import os
from pathlib import Path
from extract_manager import GeometryExtractManager

def create_mock_raw_data(output_dir):
    """SCDM이 없어도 테스트할 수 있게 가짜 raw_data.csv를 생성합니다."""
    raw_csv = Path(output_dir) / "raw_data.csv"
    
    # 헤더 정의
    headers = [
        "Name", "Type", "Z_Center", "Volume", "MassCenter_Z", 
        "Ixx", "Iyy", "Izz", "OD_Avg", "OD_Min", "OD_Max", 
        "ID_Avg", "ID_Min", "ID_Max", "Thickness"
    ]
    
    # 가짜 데이터 (Cylinder 하나, Plate 하나)
    data = [
        # Name, Type, Z_C, Vol, CG_Z, Ixx, Iyy, Izz, OD_A, OD_Mi, OD_Ma, ID_A, ID_Mi, ID_Ma, Thk
        ["Shaft_A", "Cylinder", "75.0", "1500000.0", "75.0", "1000", "1000", "500", "100.0", "98.0", "102.0", "80.0", "79.0", "81.0", "0"],
        ["Disk_B", "Plate", "160.0", "500000.0", "160.0", "2000", "2000", "4000", "300.0", "0", "0", "0", "0", "0", "20.0"]
    ]
    
    with open(raw_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Mock data created at {raw_csv}")

if __name__ == "__main__":
    # 1. 테스트용 디렉토리 및 설정 준비
    test_dir = "./test_output"
    os.makedirs(test_dir, exist_ok=True)
    
    # 임시 config 파일 생성
    import json
    config = {
        "scdm_path": "dummy",
        "geometry_file": "dummy.scdoc",
        "output_dir": test_dir,
        "sections": [
            {"name": "Shaft_A", "type": "Cylinder", "z_start": 0, "z_end": 150, "density": 7850, "tuning_margin": 0.2},
            {"name": "Disk_B", "type": "Plate", "z_start": 150, "z_end": 170, "density": 7850, "tuning_margin": 0.1}
        ]
    }
    config_path = os.path.join(test_dir, "test_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f)

    # 2. Mock raw_data 생성 (SCDM이 한 것으로 가정)
    create_mock_raw_data(test_dir)

    # 3. Refinement 로직 실행
    manager = GeometryExtractManager(config_path)
    manager.refine_data()
    
    print("\n--- Test Finished ---")
    print(f"Please check {test_dir}/final_parameters.csv to see the ton-mm results and tuning ranges.")
