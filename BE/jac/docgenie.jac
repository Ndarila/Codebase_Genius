# docgenie.jac
# DocGenie - writes final markdown docs and a simple SVG diagram

py_module doc_writer from "../py_modules/doc_writer.py" as dw
py_module diagram_generator from "../py_modules/diagram_generator.py" as dg

walker generate_docs(repo_name: str, readme_summary: str, file_list: list, analyses: map, output_dir: str) -> str:
    ::print("DocGenie: writing docs to " + output_dir)
    docs_path = dw.write_docs(output_dir, repo_name, readme_summary, file_list, analyses)
    # simple node list for diagram (max 50)
    nodes = []
    i = 0
    for f in file_list:
        if i >= 50:
            break
        nodes.append(f.split("/").last())
        i = i + 1
    svg_path = dg.generate_simple_ccg(output_dir, repo_name, nodes)
    ret docs_path
