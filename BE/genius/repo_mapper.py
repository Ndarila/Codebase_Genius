import os
import shutil
import subprocess
from typing import List, Dict


def clone_or_copy(repo: str, dest_root: str = './tmp_repos') -> str:
    os.makedirs(dest_root, exist_ok=True)
    if os.path.isdir(repo):
        name = os.path.basename(os.path.abspath(repo))
        dest = os.path.join(dest_root, name)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(repo, dest)
        return dest
    # assume git URL
    name = repo.rstrip('/').split('/')[-1].replace('.git', '')
    dest = os.path.join(dest_root, name)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    subprocess.check_call(['git', 'clone', repo, dest])
    return dest


def build_file_tree(root: str) -> List[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip unwanted dirs
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', '__pycache__')]
        for f in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, f), root))
    files.sort()
    return files


def summarize_readme(root: str) -> str:
    candidates = [p for p in os.listdir(root) if p.lower().startswith('readme')]
    if not candidates:
        return 'No README found.'
    path = os.path.join(root, candidates[0])
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            text = fh.read()
    except Exception:
        return 'README exists but could not be read.'
    # simple heuristic: first 6 non-empty lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return '\n'.join(lines[:6]) if lines else 'README empty.'
