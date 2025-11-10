# Minimal runnable Jac example: defines a walker and spawns it from entry

walker simple_walker {
    has repo_url: str;

    # Entry ability runs when walker is spawned
    can start with entry {
        print("simple_walker started with: " + self.repo_url);
        # simulate small work
        print("simple_walker finished");
    }
}

with entry {
    # spawn the walker at root with a repo url (change as needed)
    simple_walker("https://example.com/repo") spawn root;
}
