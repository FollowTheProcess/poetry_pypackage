#!/usr/bin/env python3

import shutil
import subprocess
import sys
from pathlib import Path

# Absolute path to the project root
HERE = Path.cwd().resolve()


def run(*args: str) -> None:
    """
    Helper function to run a subprocess command
    easily.
    """
    subprocess.run([*args], check=True, cwd=HERE)


def main() -> int:
    """
    Main routine.

    Returns:
        int: Exit code
    """

    if "{{cookiecutter.use_gh_cli_to_create_repo}}" != "y":
        # Do nothing and exit with success code so cookiecutter continues
        return 0

    # User said yes

    # Check whether the gh cli is installed.
    if not bool(shutil.which("gh")):
        print("Error: gh CLI not installed. Cannot create repo.")
        return 1

    # If we get here we're fine, cookiecutter will check for git itself

    # Set up a local git repo and make an initial commit
    run("git", "init", "--initial-branch=main")
    run("git", "add", "-A")
    run("git", "commit", "-m", "Initial Commit (Automated at Project Creation)")

    # Create a GitHub repo using the gh CLI
    # This also takes care of adding it as an origin
    run(
        "gh",
        "repo",
        "create",
        "{{cookiecutter.project_slug}}",
        "--confirm",
        "--description",
        "{{cookiecutter.project_short_description}}",
        "--public",
    )

    # Push the inital commit
    run("git", "push", "--set-upstream", "origin", "main")

    # Exit with success
    return 0


if __name__ == "__main__":
    sys.exit(main())
