# doc_writer.py
import os
import json

def write_docs(output_dir, repo_name, readme_summary, file_list, analyses):
    os.makedirs(output_dir, exist_ok=True)
    docs_path = os.path.join(output_dir, "docs.md")
    with open(docs_path, "w", encoding="utf-8") as f:
        f.write(f"# {repo_name} — Auto-generated Documentation\\n\\n")
        f.write("## Overview\\n\\n")
        f.write(readme_summary + "\\n\\n")
        f.write("## File tree (top-level sample)\\n\\n")
        for fn in file_list[:100]:
            f.write("- " + fn + "\\n")
        f.write("\\n## Analyses\\n\\n")
        for k,v in analyses.items():
            f.write(f"### {k}\\n\\n")
            if "summary" in v:
                f.write(v["summary"] + "\\n\\n")
            if "detail" in v:
                try:
                    f.write("Functions: " + ", ".join(v["detail"].get("functions",[])) + "\\n\\n")
                except Exception:
                    pass
    return docs_path
