import sys
import os
import cadquery as cq
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.strategy_planner import StrategyPlanner
from validator.engine import ValidationEngine

def generate_svg(model, filename, view_dir=(1, 1, 1)):
    """Export model to SVG with specific projection direction"""
    try:
        opt = {
            "width": 400, "height": 400,
            "showAxes": True, "projectionDir": view_dir,
            "strokeWidth": 0.5, "strokeColor": (0, 0, 0),
            "hiddenColor": (200, 200, 200), "showHidden": False
        }
        cq.exporters.export(model, filename, opt=opt)
        return True
    except Exception as e:
        print(f"Error exporting SVG {filename}: {e}")
        return False

def process_and_report():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_dir = os.path.join(project_root, "input")
    report_dir = os.path.join(project_root, "examples", "report")
    img_dir = os.path.join(report_dir, "images")
    
    if not os.path.exists(img_dir): os.makedirs(img_dir)
        
    input_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(".step")])
    validator = ValidationEngine()
    
    total_score = 0
    total_bodies = 0
    html_cases = ""
    
    views = [("Top", (0, 0, 1)), ("Front", (0, -1, 0)), ("Iso", (1, 1, 1))]
    log = {}

    for base_name in input_files:
        # Initial log entry
        log[base_name] = {"status": "IN_PROGRESS", "score": 0, "bodies": 0}
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "progress_log.json")
        with open(log_path, "w", encoding="utf-8") as f:
            import json
            json.dump(log, f, indent=4)
        full_path = os.path.join(input_dir, base_name)
        print(f"Processing {base_name} with Expert Strategy...")
        
        model = cq.importers.importStep(full_path)
        planner = StrategyPlanner(model, max_bodies=30, max_time=8, target_score=80, min_vol_ratio=1/30)
        results = planner.plan_and_execute()
        
        val_result = validator.validate_split(model, results)
        hex_score = val_result["hex_readiness"]["average_score"]
        total_score += hex_score
        total_bodies += len(results)
        
        status_class = "pass" if val_result["overall_status"] == "PASS" else "fail"
        score_color = "#2ecc71" if hex_score > 80 else ("#f1c40f" if hex_score > 60 else "#e74c3c")
        
        case_id = base_name.replace(".", "_")
        html_cases += f'''
        <div class="case">
            <div class="case-title">{base_name} <span class="status-badge {status_class}">{val_result["overall_status"]}</span></div>
            <div class="score-tag" style="color: {score_color}">Hex Mesh 적합도 점수: {hex_score:.1f} / 100</div>
            <div style="margin-top: 10px; color: #666;">부피 오차: {val_result["volume"]["diff"]:.2e} | 바디 개수: {len(results)}</div>
            
            <div class="view-container">
                <div class="view-group">
                    <div class="tag before">분할 전 (Before)</div>
                    <div style="display: flex; gap: 10px;">
        '''
        for v_name, v_dir in views:
            img_name = f"{case_id}_before_{v_name}.svg"
            generate_svg(model, os.path.join(img_dir, img_name), v_dir)
            html_cases += f'<div class="view-box"><img src="images/{img_name}"><div class="view-label">{v_name}</div></div>'
        
        html_cases += '</div></div><div class="view-group">'
        html_cases += '<div class="tag after">분할 후 (After)</div><div style="display: flex; gap: 10px;">'
        log[base_name] = {"status": "DONE", "score": hex_score, "bodies": len(results)}
        
        # Incremental Save
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        log_path = os.path.join(root_dir, "progress_log.json")
        with open(log_path, "w", encoding="utf-8") as f:
            import json
            json.dump(log, f, indent=4)
        print(f"   💾 Saved {base_name} score to progress_log.json")

        if not results:
            print(f"   ! No results for {base_name}")
            continue
            
        combined = results[0]
        for b in results[1:]: combined = combined.add(b)
        for v_name, v_dir in views:
            img_name = f"{case_id}_after_{v_name}.svg"
            generate_svg(combined, os.path.join(img_dir, img_name), v_dir)
            html_cases += f'<div class="view-box"><img src="images/{img_name}"><div class="view-label">{v_name}</div></div>'
            
        html_cases += '</div></div></div></div>'

    avg_overall = total_score / len(input_files) if input_files else 0
    
    html_template = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Solid Split CadQuery - AI Expert Analysis Report</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Noto Sans KR', sans-serif; margin: 40px; background-color: #f0f2f5; color: #333; }}
            .container {{ max-width: 1200px; margin: auto; }}
            .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }}
            .summary-card {{ background: white; border-radius: 10px; padding: 20px; display: flex; gap: 20px; margin-bottom: 30px; border-left: 5px solid #3498db; }}
            .summary-item {{ flex: 1; text-align: center; }}
            .summary-val {{ font-size: 2.5em; font-weight: bold; color: #2c3e50; }}
            .case {{ background: white; border-radius: 12px; padding: 25px; margin-bottom: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .case-title {{ font-size: 1.6em; font-weight: 700; color: #2c3e50; margin-bottom: 10px; }}
            .status-badge {{ padding: 2px 12px; border-radius: 20px; font-size: 0.6em; vertical-align: middle; }}
            .pass {{ background: #e6fffa; color: #319795; }}
            .fail {{ background: #fff5f5; color: #e53e3e; }}
            .score-tag {{ font-size: 1.3em; font-weight: bold; }}
            .view-container {{ display: flex; flex-direction: column; gap: 20px; margin-top: 20px; }}
            .view-box {{ border: 1px solid #edf2f7; border-radius: 8px; padding: 5px; background: #f8fafc; text-align: center; }}
            img {{ width: 300px; height: 300px; object-fit: contain; }}
            .tag {{ padding: 4px 12px; border-radius: 4px; font-size: 0.8em; font-weight: bold; color: white; margin-bottom: 8px; display: inline-block; }}
            .before {{ background: #718096; }}
            .after {{ background: #48bb78; }}
            .view-label {{ font-size: 0.8em; color: #718096; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Solid Split CadQuery - AI Expert Analysis Report</h1>
                <p>Geometric Decomposition for High-Fidelity Hex Meshing</p>
            </div>
            <div class="summary-card">
                <div class="summary-item"><div>Total Cases</div><div class="summary-val">{len(input_files)}</div></div>
                <div class="summary-item"><div>Avg Hex Score</div><div class="summary-val" style="color: #f6ad55;">{avg_overall:.1f}</div></div>
                <div class="summary-item"><div>Total Bodies</div><div class="summary-val">{total_bodies}</div></div>
            </div>
            {html_cases}
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(report_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_template)
        
    # Save the progress log to a file (Guaranteed Absolute path)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    log_path = os.path.join(root_dir, "progress_log.json")
    
    print(f"💾 Root Directory: {root_dir}")
    print(f"💾 Saving progress log ({len(log)} entries) to {log_path}...")
    with open(log_path, "w", encoding="utf-8") as f:
        import json
        json.dump(log, f, indent=4)
        
    print("✅ Final Expert Report and Progress Log Generated!")

if __name__ == "__main__":
    process_and_report()
