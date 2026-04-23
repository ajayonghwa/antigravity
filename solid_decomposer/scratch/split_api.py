# -*- coding: utf-8 -*-
import os

source = r"/Users/yonghwaheo/Documents/antigravity/solid_decomposer/reference/SpaceClaim.Api.V22.md"
output_dir = r"/Users/yonghwaheo/Documents/antigravity/solid_decomposer/reference/api_summary"

categories = {
    "Geometry": ["Geometry", "Frame", "Point", "Direction", "Matrix", "Circle", "Curve"],
    "Commands": ["Commands", "SplitBody", "Fill", "ExtrudeEdges", "MoveToComponent"],
    "Modeler": ["Modeler", "Part", "Component", "DesignBody", "Face", "Edge", "Shape"],
    "Scripting": ["Scripting", "Selection", "Window", "Application"]
}

# Ensure dir exists
if not os.path.exists(output_dir): os.makedirs(output_dir)

category_files = {k: open(os.path.join(output_dir, "API_" + k + ".md"), "w") for k in categories}

with open(source, "r") as f:
    current_block = []
    current_category = None
    
    for line in f:
        if line.strip() == "- **member**":
            # Process previous block
            if current_category and current_block:
                category_files[current_category].write("".join(current_block) + "\n---\n")
            
            current_block = [line]
            current_category = None
        else:
            current_block.append(line)
            # Match: - *@name:* `X:SpaceClaim.Api.V22.
            if "- *@name:* `" in line and "SpaceClaim.Api.V22." in line:
                for cat, keywords in categories.items():
                    if any(kw in line for kw in keywords):
                        current_category = cat
                        break

# Close files
for f in category_files.values(): f.close()
print("API Split Complete.")
