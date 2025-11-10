import supervisor;

with entry:
    repo = "https://github.com/jaseci-labs/jaseci"
    ::print("Invoking supervisor for " + repo)
    result = supervisor::supervisor_run(repo)
    ::print("Supervisor returned: " + result)
