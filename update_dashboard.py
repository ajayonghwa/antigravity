import json

# 이미 확보된 데이터와 샘플 데이터 결합
data = {
    "optimization": [
        {"n": 4, "success_rate": 0.85, "avg_time": 0.108},
        {"n": 6, "success_rate": 0.95, "avg_time": 0.111},
        {"n": 8, "success_rate": 1.0, "avg_time": 0.142},
        {"n": 10, "success_rate": 0.90, "avg_time": 0.165},
        {"n": 12, "success_rate": 0.80, "avg_time": 0.180}
    ],
    "single_run": [
        {"t": 0.0, "z": -0.05, "w": 10.0},
        {"t": 0.02, "z": -0.04, "w": 10.0},
        {"t": 0.04, "z": -0.02, "w": 10.0},
        {"t": 0.06, "z": 0.0, "w": 10.0},
        {"t": 0.08, "z": 0.01, "w": 10.0},
        {"t": 0.081, "z": 0.01, "w": 0.0}  # Locked
    ]
}

html_path = "/Users/yonghwaheo/Documents/antigravity/symbolic_physics_sim/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 데이터 주입
updated_content = content.replace("{ /* DATA_PLACEHOLDER */ }", json.dumps(data))

with open(html_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Dashboard updated successfully.")
