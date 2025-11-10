# Archived: original `quick_supervisor_good.jac`

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

    ret docs_path

with entry {
    quick_supervisor("https://github.com/jaseci-labs/jaseci") spawn root;
}
