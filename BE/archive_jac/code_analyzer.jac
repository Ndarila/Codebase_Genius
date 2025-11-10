# Archived: original `code_analyzer.jac`
# Content captured for archival purposes.

/*
Source (archived):

*/

// Original content from code_analyzer.jac
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
