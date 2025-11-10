import os
import argparse
from codegen.utils import clone_repo, list_files, read_file, parse_python_file, write_docs, generate_simple_ccg


def run(repo_source: str, dest_root: str = './tmp_repos', outputs_root: str = './outputs'):
    # repo_source may be a local path or a remote git url
    local_path = clone_repo(repo_source, dest_root)
    repo_name = os.path.basename(local_path)
    files = list_files(local_path)

    # try to find README
    readme_text = ''
    for f in files:
        if f.lower().endswith('readme.md') or f.lower().endswith('readme'):
            readme_text = read_file(os.path.join(local_path, f))
            break
    summary = readme_text[:800] if readme_text else 'No README found.'

    # analyze top files (limit)
    analyses = {}
    count = 0
    for f in files:
        if count >= 50:
            break
        if f.lower().endswith('.py'):
            content = read_file(os.path.join(local_path, f))
            analyses[f] = parse_python_file(content)
            count += 1

    output_dir = os.path.join(outputs_root, repo_name)
    docs_path = write_docs(output_dir, repo_name, summary, files, analyses)

    nodes = [p.split(os.sep)[-1] for p in files[:50]]
    svg_path = generate_simple_ccg(output_dir, repo_name, nodes)

    print(f"Done. Docs: {docs_path}, Diagram: {svg_path}")
    return docs_path, svg_path


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', help='Local path or git URL to analyze')
    ap.add_argument('--dest-root', default='./tmp_repos')
    ap.add_argument('--outputs-root', default='./outputs')
    args = ap.parse_args()
    run(args.repo, args.dest_root, args.outputs_root)
import os
import argparse
from codegen.utils import clone_repo, list_files, read_file, parse_python_file, write_docs, generate_simple_ccg


def run(repo_source: str, dest_root: str = './tmp_repos', outputs_root: str = './outputs'):
    # repo_source may be a local path or a remote git url
    local_path = clone_repo(repo_source, dest_root)
    repo_name = os.path.basename(local_path)
    files = list_files(local_path)

    # try to find README
    readme_text = ''
    for f in files:
        if f.lower().endswith('readme.md') or f.lower().endswith('readme'):
            readme_text = read_file(os.path.join(local_path, f))
            break
    summary = readme_text[:800] if readme_text else 'No README found.'

    # analyze top files (limit)
    analyses = {}
    count = 0
    for f in files:
        if count >= 50:
            break
        if f.lower().endswith('.py'):
            content = read_file(os.path.join(local_path, f))
            analyses[f] = parse_python_file(content)
            count += 1

    output_dir = os.path.join(outputs_root, repo_name)
    docs_path = write_docs(output_dir, repo_name, summary, files, analyses)

    nodes = [p.split(os.sep)[-1] for p in files[:50]]
    svg_path = generate_simple_ccg(output_dir, repo_name, nodes)

    print(f"Done. Docs: {docs_path}, Diagram: {svg_path}")
    return docs_path, svg_path


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', help='Local path or git URL to analyze')
    ap.add_argument('--dest-root', default='./tmp_repos')
    ap.add_argument('--outputs-root', default='./outputs')
    args = ap.parse_args()
    run(args.repo, args.dest_root, args.outputs_root)
