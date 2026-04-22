import ollama
import json
from geometry_generator import GeometryGenerator
from mesh_evaluator import MeshEvaluator

class OllamaStrategist:
    """
    로컬 Ollama(Gemma) 모델을 사용하여 분할 전략을 생성하고 평가받는 클래스.
    """
    def __init__(self, model_name="gemma4:e4b"):
        self.model_name = model_name
        self.generator = GeometryGenerator()
        self.evaluator = MeshEvaluator()

    def solve_problem(self, level=1, max_attempts=2):
        # 1. 문제 생성
        problem = self.generator.generate_problem(level)
        print(f"\n[Level {level}] Solving: {problem['name']}")
        
        messages = [
            {'role': 'system', 'content': 'You are an expert FEA engineer. Respond ONLY in valid JSON format.'},
            {'role': 'user', 'content': self._build_prompt(problem)}
        ]

        for attempt in range(max_attempts):
            print(f"Attempt {attempt+1}: Thinking with {self.model_name}...")
            response = ollama.chat(model=self.model_name, messages=messages)
            
            try:
                content = response['message']['content']
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                
                # JSON 결과가 리스트일 수도 있으므로 처리
                plans = json_str if isinstance(json_str, list) else json.loads(json_str)
                if isinstance(plans, dict): plans = [plans]
                
                total_score = 0
                for plan in plans:
                    total_score += self.evaluator.calculate_score(problem, plan)
                
                avg_score = total_score / len(plans) if plans else 0
                print(f"   ㄴ AI Proposed {len(plans)} plans. Avg Score: {avg_score:.2f}/100.00")
                
                if avg_score >= 90:
                    print("   ㄴ Great strategy found!")
                    return avg_score
                
                # 점수가 낮을 경우 피드백을 주고 다음 시도 진행
                messages.append({'role': 'assistant', 'content': json_str})
                feedback = f"Your previous score was {score:.2f}. The plane is not perfectly aligned or centered. Please improve the origin and normal coordinates for 100 points."
                messages.append({'role': 'user', 'content': feedback})
                
            except Exception as e:
                print(f"   ㄴ Error parsing response: {e}")
                print(f"--- RAW RESPONSE START ---\n{content}\n--- RAW RESPONSE END ---")
                messages.append({'role': 'user', 'content': "Invalid JSON format. Please provide ONLY the JSON object."})
        
        return 0

    def _build_prompt(self, problem):
        return f"""Analyze this 3D geometry JSON and provide a COMPREHENSIVE split strategy for Hexahedral meshing.
You can propose MULTIPLE split planes to isolate different features (Tapers, CrossHoles, etc.).

Geometry: {json.dumps(problem)}

Response must be a JSON LIST of split objects:
[
  {{
    "strategy": "SECTOR" or "AXIAL" or "TRANSVERSE",
    "split_plane": {{ "origin": [x,y,z], "normal": [nx,ny,nz] }},
    "reasoning": "..."
  }},
  ...
]
"""

if __name__ == "__main__":
    strategist = OllamaStrategist()
    # 보스 레벨 (Lv.11) 최종 테스트
    strategist.solve_problem(level=11, max_attempts=1)
