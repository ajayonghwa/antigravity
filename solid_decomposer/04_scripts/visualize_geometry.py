# -*- coding: utf-8 -*-
import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# JSON 데이터 경로 (사용자 환경에 맞춰 자동 감지 시도)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_ROOT, "data", "geometry_data.json")

def visualize():
    if not os.path.exists(JSON_PATH):
        print(f"[ERROR] JSON file not found: {JSON_PATH}")
        return

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    found_holes = 0
    for body in data.get("bodies", []):
        for face in body.get("faces", []):
            orig = face.get("origin", [0,0,0])
            rad = face.get("radius", 0.0)
            
            if rad > 0:
                # 구멍 시각화 (빨간색 원)
                ax.scatter(orig[0], orig[1], orig[2], color='red', s=50, label='Hole' if found_holes == 0 else "")
                
                # 구멍 주변에 간단한 원 그리기 (XY 평면 기준 가정)
                theta = np.linspace(0, 2*np.pi, 20)
                x = orig[0] + rad * np.cos(theta)
                y = orig[1] + rad * np.sin(theta)
                z = np.full_like(x, orig[2])
                ax.plot(x, y, z, color='red', alpha=0.5)
                found_holes += 1
            else:
                # 일반 면 중심점 (회색 점)
                ax.scatter(orig[0], orig[1], orig[2], color='gray', s=10, alpha=0.3)

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title(f"SCDM Geometry Visualization\nDetected Holes: {found_holes}")
    
    if found_holes > 0:
        plt.legend()
    
    print(f"[SUCCESS] Visualizing {found_holes} holes. Close the window to exit.")
    plt.show()

if __name__ == "__main__":
    visualize()
