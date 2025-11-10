import os
import shutil
import subprocess
import ast
from typing import List, Dict, Any


def clone_repo(repo_url: str, dest_root: str) -> str:
    """Clone a git repo to dest_root/<repo_name>. If repo_url is a local path, copy it."""
    os.makedirs(dest_root, exist_ok=True)
    if os.path.isdir(repo_url):
        # treat as local path
        repo_name = os.path.basename(os.path.abspath(repo_url))
        local_path = os.path.join(dest_root, repo_name)
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        shutil.copytree(repo_url, local_path)
        return local_path

    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    local_path = os.path.join(dest_root, repo_name)
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    subprocess.check_call(['git', 'clone', repo_url, local_path])
    return local_path


def list_files(root: str) -> List[str]:
    res = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            res.append(rel)
    res.sort()
    return res


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        return fh.read()


def parse_python_file(src_text: str) -> Dict[str, Any]:
    """Return a simple analysis: list of functions, classes, and calls."""
    try:
        tree = ast.parse(src_text)
    except Exception as e:
        return {"error": str(e), "functions": [], "classes": [], "calls": []}

    funcs = []
    classes = []
    calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Call):
            # try to get call name
            fn = node.func
            if isinstance(fn, ast.Name):
                calls.append(fn.id)
            elif isinstance(fn, ast.Attribute):
                calls.append(fn.attr)

    return {"functions": funcs, "classes": classes, "calls": calls}


def write_docs(output_dir: str, repo_name: str, readme_summary: str, file_list: List[str], analyses: Dict[str, Any]) -> str:
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'docs.md')
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(f"# {repo_name} - Auto docs\n\n")
        fh.write("## README summary\n\n")
        fh.write(readme_summary + "\n\n")
        fh.write("## Files analyzed\n\n")
        for f in file_list:
            fh.write(f"- {f}\n")
        fh.write("\n## Analyses\n\n")
        for f, a in analyses.items():
            fh.write(f"### {f}\n")
            if isinstance(a, dict) and 'error' in a:
                fh.write(f"Error parsing: {a['error']}\n\n")
                continue
            fh.write(f"Functions: {len(a.get('functions', []))}\n\n")
            fh.write(f"Classes: {len(a.get('classes', []))}\n\n")
    return out_path


def generate_simple_ccg(output_dir: str, repo_name: str, nodes: List[str]) -> str:
    os.makedirs(output_dir, exist_ok=True)
    svg_path = os.path.join(output_dir, 'diagram.svg')
    # Very small SVG listing file nodes vertically
    lines = [f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"400\" height=\"{20 + 20*len(nodes)}\">\n"]
    y = 20
    for n in nodes:
        safe = (n[:40] + '...') if len(n) > 40 else n
        lines.append(f"<text x=\"10\" y=\"{y}\" font-family=\"sans-serif\" font-size=\"12\">{safe}</text>\n")
        y += 20
    lines.append("</svg>\n")
    with open(svg_path, 'w', encoding='utf-8') as fh:
        fh.writelines(lines)
    return svg_path
