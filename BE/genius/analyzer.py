import ast
from typing import Dict, List, Any


def analyze_python_source(src_text: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(src_text)
    except Exception as e:
        return {"error": str(e), "functions": [], "classes": [], "calls": [], "calls_map": {}}

    funcs = []
    classes = []
    calls = []
    calls_map = {}

    current_fn = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.append(node.name)
            current_fn = node.name
            calls_map.setdefault(node.name, [])
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Call):
            fn = node.func
            name = None
            if isinstance(fn, ast.Name):
                name = fn.id
            elif isinstance(fn, ast.Attribute):
                name = fn.attr
            if name:
                calls.append(name)
                if current_fn:
                    calls_map.setdefault(current_fn, []).append(name)

    return {"functions": funcs, "classes": classes, "calls": calls, "calls_map": calls_map}


def build_ccg_for_files(file_contents: Dict[str, str]) -> Dict[str, Any]:
    # returns nodes (functions/classes) and edges (caller -> callee)
    nodes = set()
    edges = []
    analyses = {}
    for path, src in file_contents.items():
        res = analyze_python_source(src)
        analyses[path] = res
        for f in res.get('functions', []):
            nodes.add(f)
        for c in res.get('classes', []):
            nodes.add(c)
        for caller, callees in res.get('calls_map', {}).items():
            for callee in callees:
                edges.append((caller, callee))
    return {"nodes": list(nodes), "edges": edges, "analyses": analyses}
