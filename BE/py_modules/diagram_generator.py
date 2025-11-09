# diagram_generator.py
import os

def generate_simple_ccg(output_dir, repo_name, nodes):
    os.makedirs(output_dir, exist_ok=True)
    svg_path = os.path.join(output_dir, "ccg.svg")
    # simple SVG boxes for the first N nodes
    width = 800
    height = max(200, 30 * len(nodes))
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\\n')
        y = 20
        for n in nodes:
            f.write(f'<rect x="10" y="{y}" width="780" height="24" style="fill:#e8f0ff;stroke:#1f4b8f;stroke-width:1"/>\\n')
            f.write(f'<text x="18" y="{y+16}" font-size="12" font-family="Arial">{n}</text>\\n')
            y += 30
        f.write("</svg>")
    return svg_path
