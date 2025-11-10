# API Helper module for Codebase Genius
# Simple utility walker to display API usage instructions

# API Helper for Codebase Genius
walker api_helper {
    has repo: str;
    can start with entry {
        std.out("To analyze via API:");
        std.out("1. Start the server:");
        std.out("   cd BE/genius");
        std.out("   python3 api.py");
        std.out("");
        std.out("2. Send request:");
        std.out("   curl -X POST http://localhost:8000/run");
        std.out("        -H 'Content-Type: application/json'");
        std.out("        -d repo=" + repo);
    }
}