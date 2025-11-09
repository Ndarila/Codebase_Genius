# supervisor.jac
# Supervisor (Code Genius) - orchestrates mapping, analysis and doc generation

import "repo_mapper.jac" as mapper
import "code_analyzer.jac" as analyzer
import "docgenie.jac" as doc

walker supervisor_run(url: str) -> str:
    ::print("Supervisor: starting pipeline for " + url)

    # 1) clone + map
    map_result = mapper::map_repo(url)
    ::print("Supervisor: mapper returned")

    # basic checks
    if not map_result:
        ret "Error: mapper failed."

    file_list = map_result["files"]
    readme_summary = map_result["readme_summary"]
    repo_name = map_result["repo_name"]
    local_path = map_result["local_path"]
    output_dir = map_result["output_dir"]

    # 2) analyze top files (first 5 non-empty)
    analyses = {}
    i = 0
    for f in file_list:
        if i >= 5:
            break
        # skip binary-ish files by extension
        if f.lower().ends_with(".png") or f.lower().ends_with(".jpg") or f.lower().ends_with(".ico"):
            continue
        analysis = analyzer::analyze_file(local_path, f)
        analyses[f] = analysis
        i = i + 1

    # 3) generate docs (DocGenie)
    out = doc::generate_docs(repo_name, readme_summary, file_list, analyses, output_dir)
    ::print("Supervisor: docs generated at " + out)

    ret out
