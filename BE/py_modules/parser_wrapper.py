# parser_wrapper.py
import ast

def parse_python_file(src_text):
    """Return simple structure: list of function names and class names + simple calls inside functions."""
    try:
        tree = ast.parse(src_text)
    except Exception:
        return {"functions": [], "classes": [], "calls": []}

    functions = []
    classes = []
    calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            # find calls inside:
            inner_calls = []
            for n in ast.walk(node):
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Name):
                        inner_calls.append(n.func.id)
                    elif isinstance(n.func, ast.Attribute):
                        inner_calls.append(n.func.attr)
            calls.append({"function": node.name, "calls": inner_calls})
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {"functions": functions, "classes": classes, "calls": calls}
