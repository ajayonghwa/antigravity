import os
import json
import subprocess

class ExtractManager:
    def __init__(self, project_root):
        self.project_root = project_root
        self.data_dir = os.path.join(project_root, "data")
        self.extractor_script = os.path.join(project_root, "extractor", "scdm_extractor.py")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def prepare_scdm_script(self, output_json_name="geometry_data.json"):
        """
        SCDM 스크립트 내의 출력 경로를 현재 환경에 맞게 수정합니다.
        (실제로는 템플릿 치환 방식을 권장합니다)
        """
        output_path = os.path.join(self.data_dir, output_json_name)
        # Windows 경로 호환성을 위해 backslash 처리
        win_output_path = output_path.replace("/", "\\")
        
        # 실제 환경에서는 scdm_extractor.py를 읽어서 경로 부분을 수정하는 로직이 들어갑니다.
        return win_output_path

    def load_geometry_data(self, json_name="geometry_data.json"):
        """
        SCDM에서 추출된 JSON 데이터를 로드합니다.
        """
        json_path = os.path.join(self.data_dir, json_name)
        if not os.path.exists(json_path):
            print(f"Error: {json_path} not found.")
            return None
            
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    # 테스트 코드
    manager = ExtractManager(os.getcwd())
    print(f"Ready to extract data to: {manager.data_dir}")
