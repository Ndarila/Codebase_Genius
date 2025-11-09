# repo_mapper.jac
# Repo Mapper - clones a GitHub repo and returns a light map

py_module repo_utils from "../py_modules/repo_utils.py" as ru

walker map_repo(url: str) -> map:
    ::print("Repo Mapper: cloning " + url)
    tmp_root = "./tmp_repos"
    # call Python helper to clone repo
    local_path = ru.clone_repo(url, tmp_root)
    files = ru.list_files(local_path)

    # try to find README file (case-insensitive)
    readme_path = ""
    for f in files:
        lower = f.lower()
        if lower.ends_with("readme.md") or lower.ends_with("readme"):
            readme_path = f
            break

    readme_text = ""
    if readme_path != "":
        readme_text = ru.read_file(local_path + "/" + readme_path)

    summary = readme_text[:800] if readme_text else "No README found."

    repo_name = url.rstrip("/").split("/")[-1].replace(".git","")
    output_dir = "./outputs/" + repo_name

    out = {
        "repo_name": repo_name,
        "local_path": local_path,
        "files": files,
        "readme_summary": summary,
        "output_dir": output_dir
    }
    ret out
