import json

class AIPlanner:
    """
    AI-driven decomposition strategist.
    It takes raw geometric summaries and refines them using AI reasoning.
    """
    def __init__(self, raw_report):
        self.raw_report = raw_report

    def create_ai_prompt(self):
        """Generates a prompt for the AI to analyze the model."""
        prompt = f"""
        [CAD Geometry Analysis Request]
        Overall Size: {self.raw_report['overall_size']}
        Detected Steps: {self.raw_report['steps']}
        Detected Cylindrical Features:
        {json.dumps(self.raw_report['features'], indent=2)}
        
        Goal: Decompose this solid into high-quality hex-meshable primitives (Boxes, Cylinders).
        
        Task: 
        1. Analyze the relationship between features.
        2. Decide the priority of splits (e.g., O-GRID first to isolate a large disk).
        3. Output a refined JSON decomposition plan.
        """
        return prompt

    def apply_ai_strategy(self, ai_refined_json):
        """Parses the AI's suggestion and returns the finalized plan."""
        try:
            # AI가 준 JSON을 파싱하여 StrategyPlanner가 이해할 수 있는 형식으로 반환
            refined_plan = json.loads(ai_refined_json)
            return refined_plan
        except Exception as e:
            print(f"⚠️ Failed to parse AI strategy: {e}")
            return self.raw_report # Fallback to raw report
