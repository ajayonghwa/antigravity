import json
import os
from geometry_generator import GeometryGenerator
from mesh_evaluator import MeshEvaluator

class ResearchSandbox:
    """
    문제 생성 - 전략 수립 - 심판 채점 루프를 자동화하는 샌드박스.
    """
    def __init__(self):
        self.generator = GeometryGenerator()
        self.evaluator = MeshEvaluator()
        self.history = []

    def run_training_loop(self, start_level=1, end_level=3, iterations_per_level=2):
        print(f"=== Starting Automated Research Loop (Lv.{start_level} ~ Lv.{end_level}) ===")
        
        for lv in range(start_level, end_level + 1):
            for i in range(iterations_per_level):
                # 1. 문제 출제 (무작위 파라미터)
                problem = self.generator.generate_problem(lv)
                
                # 2. 초기 전략 수립 (일부러 약간의 오차를 섞은 시뮬레이션 가능)
                # 실제 운영시에는 여기서 LLM API를 호출하거나, Antigravity의 초기안을 사용함
                strategy = self._simulate_ai_strategy(problem, attempt=1)
                
                # 3. 채점
                score = self.evaluator.calculate_score(problem, strategy)
                
                # 4. 결과 기록
                result = {
                    "level": lv,
                    "iteration": i + 1,
                    "problem_name": problem["name"],
                    "score": score,
                    "strategy": strategy["strategy"]
                }
                self.history.append(result)
                print(f"[Lv.{lv}-{i+1}] {problem['name']} -> Score: {score:.2f}")

                # 5. 자가 교정 (Score가 낮을 경우 한 번 더 시도)
                if score < 90:
                    refined_strategy = self._simulate_ai_strategy(problem, attempt=2)
                    refined_score = self.evaluator.calculate_score(problem, refined_strategy)
                    print(f"   ㄴ Refined Attempt -> Score: {refined_score:.2f}")
                    self.history[-1]["score_refined"] = refined_score

        self._save_logs()

    def _simulate_ai_strategy(self, problem, attempt=1):
        """
        AI의 전략 수립 과정을 시뮬레이션함.
        """
        level = problem["level"]
        
        if level == 1: # Cylinder
            offset = 5.0 if attempt == 1 else 0.0
            return {
                "strategy": "SECTOR",
                "split_plane": {"origin": [offset, 0, 0], "normal": [1, 0, 0]}
            }
        elif level == 2: # Stepped
            offset = 2.0 if attempt == 1 else 0.0
            z_coord = problem["cylinders"][1]["origin"][2] + offset
            return {
                "strategy": "AXIAL",
                "split_plane": {"origin": [0, 0, z_coord], "normal": [0, 0, 1]}
            }
        elif level == 4: # T-Junction
            # T-Junction의 핵심은 분기 파이프 입구(Origin)에서의 TRANSVERSE 분할
            offset = 3.0 if attempt == 1 else 0.0
            branch_cyl = problem["cylinders"][1]
            return {
                "strategy": "TRANSVERSE",
                "split_plane": {
                    "origin": [branch_cyl["origin"][0] + offset, 0, 0],
                    "normal": [1, 0, 0]
                }
            }
        elif level == 5: # Y-Junction
            # Y-Junction은 분기 각도에 따른 정밀한 평면 설정이 핵심
            branch_cyl = problem["cylinders"][1]
            return {
                "strategy": "TRANSVERSE",
                "split_plane": {
                    "origin": branch_cyl["origin"],
                    "normal": branch_cyl["axis"]
                }
            }
        elif level >= 6: # Offset, Manifold 등 복합 형상
            # 복합 형상의 경우 첫 번째 피쳐를 기준으로 기본 전략 수립
            main_cyl = problem["cylinders"][0]
            return {
                "strategy": "TRANSVERSE",
                "split_plane": {
                    "origin": main_cyl["origin"],
                    "normal": main_cyl["axis"]
                }
            }
        else:
            return {"strategy": "UNKNOWN", "split_plane": {"origin": [0,0,0], "normal": [0,0,1]}}

    def _save_logs(self):
        log_path = "optimizer/data/research_logs.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
        print(f"=== Research Logs saved to {log_path} ===")

if __name__ == "__main__":
    sandbox = ResearchSandbox()
    # Lv.1부터 Lv.10까지 최종 자동 루프 실행 (약 10분 내외 소요 예상)
    sandbox.run_training_loop(start_level=1, end_level=10, iterations_per_level=3)
