# repo_utils.py
import os
import shutil
import subprocess

def clone_repo(url, tmp_root="./tmp_repos"):
    os.makedirs(tmp_root, exist_ok=True)
    repo_name = url.rstrip("/").split("/")[-1].replace(".git","")
    local_path = os.path.join(tmp_root, repo_name)
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    # run git clone
    subprocess.check_call(["git", "clone", url, local_path])
    return local_path

def list_files(root):
    out = []
    for base, dirs, files in os.walk(root):
        # ignore .git, node_modules
        dirs[:] = [d for d in dirs if d not in [".git","node_modules","__pycache__"]]
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), root)
            out.append(rel.replace("\\\\", "/"))
    out.sort()
    return out

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""
