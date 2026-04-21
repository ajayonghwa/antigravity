import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_boss_result(body_data, plans, output_path="boss_decomposition.png"):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 1. Bounding Box (Outer frame)
    b_min, b_max = body_data["bbox_min"], body_data["bbox_max"]
    for s, e in [([0,1,2,4,5,6,7,3], [1,2,3,0,5,6,7,4])]: # Simple edges
        pass # Simplified for prototype

    # 2. Main Body Cylinders (Z-axis)
    ax.plot([0, 0], [0, 0], [0, 200], 'k--', alpha=0.5, label="Main Axis")
    
    # 3. Top Cross Holes
    for i in range(4):
        ang = i * np.pi/2
        r = 50.0
        ax.plot([0, r*np.cos(ang)], [0, r*np.sin(ang)], [170, 170], 'b-', alpha=0.3)

    # 4. AI Proposed Split Planes
    colors = plt.cm.viridis(np.linspace(0, 1, len(plans)))
    
    for i, plan in enumerate(plans):
        o = np.array(plan["split_plane"]["origin"])
        n = np.array(plan["split_plane"]["normal"])
        n = n / np.linalg.norm(n)
        
        # Create plane grid
        size = 60
        r = np.linspace(-size, size, 2)
        if abs(n[2]) > 0.9: # Horizontal Plane (Axial/Transverse)
            x, y = np.meshgrid(r, r)
            z = np.full_like(x, o[2])
        elif abs(n[0]) > 0.9: # Vertical Plane X
            y, z = np.meshgrid(r, np.linspace(0, 200, 2))
            x = np.full_like(y, o[0])
        else: # Vertical Plane Y
            x, z = np.meshgrid(r, np.linspace(0, 200, 2))
            y = np.full_like(x, o[1])
            
        ax.plot_surface(x, y, z, color=colors[i], alpha=0.3, label=f"Plan {i+1}: {plan['strategy']}")

    ax.set_xlim(-70, 70)
    ax.set_ylim(-70, 70)
    ax.set_zlim(0, 200)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    plt.title(f"Gemma's Decomposition Plan: {body_data['name']}")
    
    # Save to file
    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")

if __name__ == "__main__":
    # Gemma가 제안한 실제 데이터
    boss_body = {
        "name": "ULTIMATE_VALVE_BODY",
        "bbox_min": [-60, -60, 0], "bbox_max": [60, 60, 200]
    }
    gemma_plans = [
        {"strategy": "AXIAL", "split_plane": {"origin": [0,0,100], "normal": [0,0,1]}},
        {"strategy": "AXIAL", "split_plane": {"origin": [0,0,150], "normal": [0,0,1]}},
        {"strategy": "SECTOR", "split_plane": {"origin": [0,0,170], "normal": [1,0,0]}},
        {"strategy": "TRANSVERSE", "split_plane": {"origin": [0,0,10], "normal": [0,0,1]}},
        {"strategy": "PLANAR", "split_plane": {"origin": [0,0,150], "normal": [1,0,0]}},
        {"strategy": "PLANAR", "split_plane": {"origin": [0,0,150], "normal": [0,1,0]}}
    ]
    visualize_boss_result(boss_body, gemma_plans)
