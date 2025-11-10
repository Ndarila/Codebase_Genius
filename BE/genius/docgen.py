import os
import json
from typing import Dict, List, Any


def write_markdown(output_dir: str, repo_name: str, readme_summary: str, files: List[str], analyses: Dict[str, Any], ccg: Dict[str, Any]) -> str:
    os.makedirs(output_dir, exist_ok=True)
    md = []
    md.append(f"# {repo_name} - Generated Documentation\n")
    md.append("## Overview\n")
    md.append(readme_summary + "\n")
    md.append("## Files\n")
    for f in files:
        md.append(f"- {f}\n")

    md.append("## Call Graph (summary)\n")
    for edge in ccg.get('edges', [])[:200]:
        md.append(f"- {edge[0]} -> {edge[1]}\n")

    md.append("\n## File Analyses\n")
    for f, a in analyses.items():
        md.append(f"### {f}\n")
        if 'error' in a:
            md.append(f"Parse error: {a['error']}\n")
            continue
        md.append(f"Functions: {len(a.get('functions', []))}\n")
        md.append(f"Classes: {len(a.get('classes', []))}\n")
        md.append('\n')

    out_md = os.path.join(output_dir, 'docs.md')
    with open(out_md, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(md))

    # also dump ccg json
    with open(os.path.join(output_dir, 'ccg.json'), 'w', encoding='utf-8') as fh:
        json.dump(ccg, fh, indent=2)

    return out_md


def generate_simple_svg(output_dir: str, repo_name: str, nodes: List[str]) -> str:
    os.makedirs(output_dir, exist_ok=True)
    svg_path = os.path.join(output_dir, 'diagram.svg')
    height = 30 + 20*len(nodes)
    lines = [f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"700\" height=\"{height}\">\n"]
    y = 20
    for n in nodes:
        safe = (n[:60] + '...') if len(n) > 60 else n
        lines.append(f"<text x=\"10\" y=\"{y}\" font-family=\"sans-serif\" font-size=\"12\">{safe}</text>\n")
        y += 20
    lines.append("</svg>\n")
    with open(svg_path, 'w', encoding='utf-8') as fh:
        fh.writelines(lines)
    return svg_path
