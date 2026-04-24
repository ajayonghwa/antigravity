import json
import requests
from loguru import logger

class AIPlanner:
    def __init__(self, endpoint="http://localhost:11434/api/generate", model="llama3"):
        self.endpoint = endpoint
        self.model = model
        self.system_prompt = """
You are an expert in CAD geometry decomposition for Finite Element Analysis (FEA).
Your goal is to take a summary of a 3D solid and propose a sequence of splitting operations to make it "Hex-Meshable".
Hex-meshable means the resulting pieces should be as close to simple blocks (6 faces) as possible.

Common strategies:
1. Symmetry Cut: If the object is symmetric, split it along the symmetry plane.
2. Hole Isolation: Isolate holes using a "Butterfly Grid" or "H-Grid" approach. This usually involves creating planar cuts around the hole.
3. Step Split: Split at levels where there is a change in thickness (steps).
4. Core Extraction: For cylindrical objects, extract the central rectangular core.

Available Operations:
- {"operation": "plane_cut", "axis": "X"|"Y"|"Z", "coordinate": float, "reason": "string"}
- {"operation": "hole_isolation", "center": [x, y, z], "radius": float, "method": "butterfly"|"grid", "reason": "string"}

Respond ONLY with a JSON object containing:
{
  "strategy_description": "A brief explanation of your plan",
  "splits": [ ... list of operations ... ]
}
"""

    def plan_splits(self, geometry_summary):
        prompt = f"Geometry Summary:\n{json.dumps(geometry_summary, indent=2)}\n\nPropose a splitting strategy."
        
        payload = {
            "model": self.model,
            "prompt": f"{self.system_prompt}\n\n{prompt}",
            "stream": False,
            "format": "json"
        }
        
        try:
            logger.info(f"Requesting AI plan from {self.endpoint} using model {self.model}...")
            response = requests.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Ollama returns the response in a 'response' field
            plan_text = result.get("response", "")
            plan_json = json.loads(plan_text)
            return plan_json
        except Exception as e:
            logger.error(f"Failed to get AI plan: {e}")
            return self._get_fallback_plan(geometry_summary)

    def _get_fallback_plan(self, summary):
        logger.warning("Using fallback heuristic plan.")
        splits = []
        # Simple heuristic: split at all steps
        for i, feat in enumerate(summary.get("features", [])):
            if feat["type"] == "step":
                splits.append({
                    "operation": "plane_cut",
                    "axis": "Z",
                    "coordinate": feat["location_z"],
                    "reason": "Split at step (fallback)"
                })
        return {
            "strategy_description": "Fallback heuristic plan due to AI failure",
            "splits": splits
        }

if __name__ == "__main__":
    # Test with sample summary
    test_summary = {
      "overall_size": [100, 100, 10],
      "features": [
        {
          "type": "hole_pattern",
          "count": 4,
          "radius": 2.5,
          "locations": [[25, 25], [25, 75], [75, 25], [75, 75]],
          "min_distance_between_holes": 5.0
        }
      ],
      "mesh_goal": "High-quality Hexahedral mesh"
    }
    
    planner = AIPlanner()
    # This will likely use fallback if Ollama is not running
    plan = planner.plan_splits(test_summary)
    print(json.dumps(plan, indent=2))
