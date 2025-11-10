# Codebase Genius - Main Jac Walker
# Analyzes code repositories and generates documentation + call graphs

walker start_pipeline {
    has repo: str;

    can start with entry {
        print("Codebase Genius: Starting analysis of " + repo);
        print("\nTo analyze your repository:");
        print("1. Start the Python backend API:");
        print("   cd BE/genius && python3 api.py");
        print("\n2. Send a POST request:");
        print("   curl -X POST http://localhost:8000/run \\");
        print("        -H 'Content-Type: application/json' \\");
        print('        -d \'{"repo": "' + repo + '"}\'');
        print("\n3. Check outputs under BE/outputs/<repo_name>/");
        print("\nPipeline ready for repo: " + repo);
    }
}

with entry {
    # Example: Analyze the sample repo
    start_pipeline('file:///home/james-ndarila/Codebase_Genius/BE/sample_repo_simple') spawn here;
}
# Codebase Genius - Main Jac Walker
walker analyzer {
    has repo: str;

    can start with entry {
        # Set default repository if none provided
        if (!repo) {
            repo = "BE/sample_repo_simple";
        }

        std.out("Codebase Genius - Analysis Pipeline");
        std.out("================================");
        std.out("Target: " + repo);
        std.out("");
        
        # Show Python runner option
        std.out("Option 1: Direct Runner");
        std.out("cd BE/genius");
        std.out("python3 runner.py " + repo);
        std.out("");
        
        # Show API option
        api_helper {
            repo: repo
        } spawn here;
        
        std.out("");
        std.out("Outputs will be in:");
        std.out("BE/outputs/" + repo.split("/").last() + "/");
        std.out("- docs.md: Documentation");
        std.out("- diagram.svg: Call graph");
    }
}

# Main entry point
with entry {
    analyzer("BE/sample_repo_simple") spawn here;
}
 
    ::print("Main: supervisor returned -> " + result)