# main.jac
# Entrypoint for Codebase Genius Jac server

import "supervisor.jac" as sup

# public walker to start processing a repository URL
walker serve_repo(url: str) -> str:
    ::print("serve_repo called with: " + url)
    res = sup::supervisor_run(url)
    ret res
