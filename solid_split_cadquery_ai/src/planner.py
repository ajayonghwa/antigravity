import json
import requests
from loguru import logger

class AIPlanner:
    """Ollama 로컬 AI를 사용하여 솔리드 분할 전략을 수립하는 플래너입니다."""
    
    def __init__(self, model="llama3", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def plan_splits(self, summary):
        """형상 요약(JSON)을 바탕으로 Ollama에 분할 계획을 요청합니다."""
        logger.info(f"Requesting AI plan from Ollama ({self.model})...")
        
        prompt = self._build_prompt(summary)
        
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=30
            )
            response.raise_for_status()
            
            # AI 응답 파싱
            ai_response_raw = response.json().get("response", "{}")
            plan = json.loads(ai_response_raw)
            
            logger.info("AI Plan successfully received and parsed.")
            return plan

        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            return self._get_fallback_plan(summary)

    def _build_prompt(self, summary):
        return f"""
You are an expert in FEM (Finite Element Method) and CAD solid decomposition.
Your goal is to propose a splitting plan to achieve a high-quality hexahedral mesh.

Geometric Summary of the target solid:
{json.dumps(summary, indent=2)}

Please provide a decomposition plan in JSON format only.
The JSON must follow this structure:
{{
  "strategy_description": "A brief name for the strategy",
  "reasoning": "Explain why you chose these split points",
  "splits": [
    {{
      "operation": "plane_cut",
      "axis": "X" | "Y" | "Z",
      "coordinate": float,
      "reason": "Why split here?"
    }}
  ]
}}
Only return the JSON object. No other text.
"""

    def _get_fallback_plan(self, summary):
        """Ollama 호출 실패 시 사용할 기본 룰 베이스 전략입니다."""
        logger.warning("Using fallback heuristic plan.")
        plan = {
            "strategy_description": "Heuristic Fallback Plan",
            "reasoning": "Ollama connection failed. Applying basic junction-based splits.",
            "splits": []
        }
        
        for feature in summary.get("features", []):
            if feature["type"] == "junction":
                plan["splits"].append({
                    "operation": "plane_cut",
                    "axis": "Z",
                    "coordinate": feature["location"][2],
                    "reason": "Junction-based heuristic split"
                })
        return plan

if __name__ == "__main__":
    # 간단한 테스트 실행
    test_summary = {"overall_size": [100, 100, 10], "features": []}
    planner = AIPlanner()
    print(json.dumps(planner.plan_splits(test_summary), indent=2))
