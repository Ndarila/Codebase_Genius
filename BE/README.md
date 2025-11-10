# Codebase Genius

A code analysis and documentation tool that uses Python AST parsing and graph generation to create documentation and call graphs for Python repositories.

## Project Overview

Codebase Genius is a hybrid Jac/Python tool that analyzes Python repositories to generate:
- Repository structure and file listing
- Code analysis including functions, classes, and their relationships
- Simple call graphs showing dependencies between components
- Markdown documentation with an overview of the codebase

The project uses a Python backend for heavy lifting (parsing, analysis, doc generation) exposed through both a CLI and HTTP API, with a minimal Jac interface for orchestration.

## Project Structure

```
BE/
├── genius/           # Python backend implementation 
│   ├── repo_mapper.py      # Clone/copy repos and build file tree
│   ├── analyzer.py        # Parse Python files and build CCG
│   ├── docgen.py         # Generate markdown docs and diagrams
│   ├── runner.py         # CLI entry point
│   └── api.py            # HTTP API (POST /run endpoint)
├── jac/             # Jac interface
│   ├── main.jac          # Main walker interface
│   └── api_helper.jac    # API usage helper
├── outputs/         # Generated documentation
│   └── sample_repo_simple/
│       ├── docs.md        # Generated documentation
│       └── diagram.svg    # Simple call graph visualization
├── sample_repo_simple/   # Sample repository for testing
└── archive_jac/     # Archived original Jac implementations
```

## Quick Start

1. **Python Setup** (3.12 recommended):
   ```bash
   # Create and activate a virtual environment
   python3 -m venv .env
   source .env/bin/activate

   # Install Jac
   pip install jaclang
   ```

2. **Run the API Server**:
   ```bash
   cd BE/genius
   PYTHONPATH=.. python3 api.py  # Starts server on port 8000
   ```

3. **Analyze a Repository** (choose one method):

   a. Using curl:
   ```bash
   curl -X POST http://localhost:8000/run \
        -H 'Content-Type: application/json' \
        -d '{"repo":"../sample_repo_simple"}'
   ```

   b. Using the Python runner:
   ```bash
   cd BE/genius
   PYTHONPATH=.. python3 runner.py ../sample_repo_simple
   ```

   c. Using the Jac helper (shows instructions):
   ```bash
   cd BE/jac
   jac run api_helper.jac
   ```

4. **View Results**:
   - Check `BE/outputs/<repo_name>/` for generated files
   - Open `docs.md` for documentation
   - Open `diagram.svg` for the call graph visualization

## Implementation Notes

### Architecture Decision: Hybrid Approach

The project uses a hybrid architecture with:
- **Python Backend**: Handles the heavy lifting (parsing, analysis, CCG generation)
- **HTTP API**: Provides a clean interface for triggering the pipeline
- **Minimal Jac Interface**: Provides usage instructions and examples

This design was chosen because:
1. The installed Jac runtime (v0.8.10) doesn't support certain syntax (py_module declarations, colon-style walkers)
2. Python's ast module and standard library provide robust tools for code analysis
3. The HTTP API allows loose coupling between components

### Generated Artifacts

The tool generates two main artifacts under `BE/outputs/<repo_name>/`:
1. `docs.md`: Markdown documentation including:
   - Repository overview
   - File structure
   - Call graph summary
   - Per-file analysis of functions and classes
2. `diagram.svg`: A simple visualization of code relationships

## Testing

A sample repository is provided at `BE/sample_repo_simple/` for testing. Run:

```bash
cd BE/genius
PYTHONPATH=.. python3 runner.py ../sample_repo_simple
```

This will generate documentation under `BE/outputs/sample_repo_simple/`.

## Legacy Code & Migration Notes

Original Jac implementations (using py_module and colon-style syntax) are preserved under `BE/archive_jac/` for reference. These files use syntax not supported by the current Jac runtime but document the original multi-walker design:

- `repo_mapper.jac`: Repository cloning and file tree mapping
- `code_analyzer.jac`: Python file parsing and analysis
- `docgenie.jac`: Documentation and diagram generation
- `supervisor.jac`: Orchestration and walker coordination
- `quick_supervisor_good.jac`: Example implementation with py_module usage

The current implementation provides equivalent functionality through the Python backend while remaining compatible with the installed Jac runtime constraints.
# Codebase Genius (backend)

This folder contains a runnable Python implementation of the Codebase Genius pipeline used for the assignment. It provides a minimal, self-contained implementation to clone/copy a repository, list files, perform lightweight Python parsing (via ast), and generate markdown documentation and a simple SVG diagram.

Quick start (run locally on the included sample repo):

1. Create and activate a Python virtual environment (optional but recommended):

```bash
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
```

2. Run the pipeline on the bundled sample repo:

```bash
python3 -m codegen.run_pipeline ./sample_repo --dest-root ./tmp_repos --outputs-root ./outputs
```

3. View generated files under `./outputs/sample_repo` (docs.md and diagram.svg).

Notes:
- This implementation uses pure Python and ast for parsing. It is intentionally minimal so it runs in constrained environments.
- There is an optional Jac shim in `jac/supervisor_brace.jac` which demonstrates a Jac-style supervisor stub.
