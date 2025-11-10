import os
from typing import Dict
from genius.repo_mapper import clone_or_copy, build_file_tree, summarize_readme
from genius.analyzer import build_ccg_for_files
from genius.docgen import write_markdown, generate_simple_svg


def run_pipeline(repo_source: str, dest_root: str = './tmp_repos', outputs_root: str = './outputs') -> Dict[str, str]:
    local = clone_or_copy(repo_source, dest_root)
    repo_name = os.path.basename(local)
    files = build_file_tree(local)
    readme = summarize_readme(local)

    # read contents for python files
    file_contents = {}
    for f in files:
        if f.lower().endswith('.py'):
            try:
                with open(os.path.join(local, f), 'r', encoding='utf-8', errors='ignore') as fh:
                    file_contents[f] = fh.read()
            except Exception:
                file_contents[f] = ''

    ccg = build_ccg_for_files(file_contents)

    output_dir = os.path.join(outputs_root, repo_name)
    md = write_markdown(output_dir, repo_name, readme, files, ccg.get('analyses', {}), ccg)
    svg = generate_simple_svg(output_dir, repo_name, ccg.get('nodes', [])[:200])

    return {'docs': md, 'diagram': svg}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('--dest-root', default='./tmp_repos')
    ap.add_argument('--outputs-root', default='./outputs')
    args = ap.parse_args()
    res = run_pipeline(args.repo, args.dest_root, args.outputs_root)
    print('Docs:', res['docs'])
    print('Diagram:', res['diagram'])
