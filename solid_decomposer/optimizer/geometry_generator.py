import random
import numpy as np

class GeometryGenerator:
    def generate_problem(self, level=11):
        if level == 11:
            return self._level_11_boss_case()
        # ... (기존 레벨 생략) ...
        return self._level_1_cylinder()

    def _level_11_boss_case(self):
        """
        보스 레벨: 단차 + 테이퍼(두께변화) + 상단 4개 대형 구멍 + 하단 다공판
        """
        main_r = 50.0
        inner_r = 40.0
        height = 200.0
        
        # 1. 메인 몸체 (실린더들)
        cyls = [
            {"name": "Upper_Body", "origin": [0,0,150], "axis": [0,0,1], "radius": main_r, "type": "Main"},
            {"name": "Taper_Start", "origin": [0,0,100], "axis": [0,0,1], "radius": 30.0, "type": "Taper"}, # 좁아지는 구간
            {"name": "Lower_Body", "origin": [0,0,50], "axis": [0,0,1], "radius": main_r, "type": "Main"}
        ]
        
        # 2. 상단 90도 간격 대형 구멍 (4개)
        for i in range(4):
            angle = i * np.pi/2
            cyls.append({
                "name": f"Top_Hole_{i}",
                "origin": [main_r * np.cos(angle), main_r * np.sin(angle), 170],
                "axis": [np.cos(angle), np.sin(angle), 0],
                "radius": 15.0,
                "type": "CrossHole"
            })
            
        # 3. 하단 다공판 (8개 작은 구멍)
        for i in range(8):
            angle = i * np.pi/4
            dist = 35.0
            cyls.append({
                "name": f"Bottom_Hole_{i}",
                "origin": [dist * np.cos(angle), dist * np.sin(angle), 10],
                "axis": [0, 0, 1],
                "radius": 5.0,
                "type": "PlateHole"
            })
            
        return {
            "level": 11,
            "name": "ULTIMATE_VALVE_BODY",
            "bbox_min": [-60, -60, 0],
            "bbox_max": [60, 60, 200],
            "cylinders": cyls
        }

if __name__ == "__main__":
    gen = GeometryGenerator()
    print(gen.generate_problem(11))
