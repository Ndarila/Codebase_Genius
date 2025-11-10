# Archived legacy Jac files with original syntax
# NOTE: These files use syntax not supported by the current runtime
# but are preserved for reference and future porting.

# =================================================================
# supervisor.jac - Original orchestrator
# =================================================================

import repo_mapper as mapper;
import code_analyzer as analyzer;
import docgenie as doc;

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
        if f.lower().ends_with(".png") or f.lower().ends_with(".jpg") or f.lower().ends_with(".ico"):
            continue
        analysis = analyzer::analyze_file(local_path, f)
        analyses[f] = analysis
        i = i + 1

    # 3) generate docs (DocGenie)
    out = doc::generate_docs(repo_name, readme_summary, file_list, analyses, output_dir)
    ::print("Supervisor: docs generated at " + out)
    ret out

# =================================================================
# repo_mapper.jac - Repository mapping
# =================================================================

py_module repo_utils from "../py_modules/repo_utils.py" as ru

walker map_repo(url: str) -> list[str]:
    ::print("RepoMapper: mapping " + url)
    
    # Clone or copy repository
    local_path = ru.clone_repo(url)
    ::print("RepoMapper: cloned to " + local_path)
    
    # Get file list
    files = ru.list_files(local_path)
    ::print("RepoMapper: found " + files.len().to_string() + " files")
    
    ret files;

# =================================================================
# code_analyzer.jac - Code analysis
# =================================================================

py_module parser_wrapper from "../py_modules/parser_wrapper.py" as pw
py_module repo_utils from "../py_modules/repo_utils.py" as ru

walker analyze_file(local_repo: str, relpath: str) -> map:
    ::print("Code Analyzer: analyzing " + relpath)
    abs_path = local_repo + "/" + relpath
    content = ru.read_file(abs_path)
    if content == "":
        ret {"error": "empty or unreadable file", "path": relpath}
    parsed = pw.parse_python_file(content)
    summary_text = "Functions: " + parsed["functions"].len().to_string() + ", Classes: " + parsed["classes"].len().to_string()
    ret {"summary": summary_text, "detail": parsed, "path": relpath}

# =================================================================
# docgenie.jac - Documentation generation
# =================================================================

py_module doc_writer from "../py_modules/doc_writer.py" as dw
py_module diagram_generator from "../py_modules/diagram_generator.py" as dg
py_module repo_utils from "../py_modules/repo_utils.py" as ru

walker generate_docs(url: str, files: list[str], analyses: map) -> str:
    ::print("DocGenie: generating docs for " + url)

    # Set output paths
    repo_name = url.split("/").last().replace(".git", "")
    output_dir = "./outputs/" + repo_name

    # Extract readme summary if present
    summary = ""
    for f in files:
        lower = f.lower()
        if lower.ends_with("readme.md") or lower.ends_with("readme"):
            summary = ru.read_file(url + "/" + f)[:800]
            break

    # Write main documentation 
    docs_path = dw.write_docs(output_dir, repo_name, summary, files, analyses)

    # Generate simple call graph visualization
    nodes = []
    edges = []
    for f, analysis in analyses.items():
        nodes.append(f.split("/").last())
        detail = analysis.get("detail", {})
        for call in detail.get("calls", []):
            edges.append([f.split("/").last(), call.split("/").last()])
    svg_path = dg.generate_simple_ccg(output_dir, repo_name, nodes)

    ::print("DocGenie: wrote docs to " + docs_path)
    ret docs_path;

# =================================================================
# quick_supervisor_good.jac - Quick implementation with py_module
# =================================================================

py_module repo_utils from "../py_modules/repo_utils.py" as ru
py_module parser_wrapper from "../py_modules/parser_wrapper.py" as pw
py_module doc_writer from "../py_modules/doc_writer.py" as dw
py_module diagram_generator from "../py_modules/diagram_generator.py" as dg

walker quick_supervisor(url: str) -> str:
    ::print("QuickSupervisor: cloning " + url)
    tmp_root = "./tmp_repos"
    local_path = ru.clone_repo(url, tmp_root)
    files = ru.list_files(local_path)
    ::print("QuickSupervisor: found " + files.len().to_string() + " files")

    # find README
    readme = ""
    for f in files:
        lower = f.lower()
        if lower.ends_with("readme.md") or lower.ends_with("readme"):
            readme = ru.read_file(local_path + "/" + f)
            break

    summary = readme[:800] if readme else "No README found."

    analyses = {}
    i = 0
    for f in files:
        if i >= 5:
            break
        if f.lower().ends_with(".png") or f.lower().ends_with(".jpg") or f.lower().ends_with(".ico"):
            continue
        content = ru.read_file(local_path + "/" + f)
        parsed = pw.parse_python_file(content)
        analyses[f] = {"summary": "Functions: " + parsed["functions"].len().to_string() + ", Classes: " + parsed["classes"].len().to_string(), "detail": parsed}
        i = i + 1

    repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
    output_dir = "./outputs/" + repo_name
    docs_path = dw.write_docs(output_dir, repo_name, summary, files, analyses)

    nodes = []
    j = 0
    for f in files:
        if j >= 50:
            break
        nodes.append(f.split("/").last())
        j = j + 1
    svg = dg.generate_simple_ccg(output_dir, repo_name, nodes)

    ::print("QuickSupervisor: docs written to " + docs_path)
    ret docs_path;