"""
Nox configuration file for the project.
"""

import json
import os
import shutil
import tempfile
import webbrowser
from pathlib import Path
from typing import Any, Dict, List

import nox

# Minimum nox version
nox.needs_version = ">=2021.6.6"

# GitHub Actions
ON_CI = bool(os.getenv("CI"))

# Global project stuff
PROJECT_ROOT = Path(__file__).parent.resolve()
PROJECT_SRC = PROJECT_ROOT / "{{cookiecutter.project_slug}}"
PROJECT_TESTS = PROJECT_ROOT / "tests"

# Where to save the coverage badge
COVERAGE_BADGE = PROJECT_ROOT / "docs" / "img" / "coverage.svg"

# VSCode
VSCODE_DIR = PROJECT_ROOT / ".vscode"
SETTINGS_JSON = VSCODE_DIR / "settings.json"

# Poetry virtual environment stuff
VENV_DIR = PROJECT_ROOT / ".venv"
PYTHON = os.fsdecode(VENV_DIR / "bin" / "python")

# Python to use for non-test sessions
DEFAULT_PYTHON: str = "3.9"

# All supported python versions for {{cookiecutter.project_slug}}
PYTHON_VERSIONS: List[str] = [
    "3.7",
    "3.8",
    "3.9",
]

# List of seed packages to upgrade to their most
# recent versions in every nox environment
# these aren't strictly required but I've found including them
# solves most installation problems
SEEDS: List[str] = [
    "pip",
    "setuptools",
    "wheel",
]

# Dependencies for each of the nox session names
# these names must be identical to the names of the defined nox sessions
# the list of dependencies here are installed against the contraints
# file generated by poetry_install
SESSION_REQUIREMENTS: Dict[str, List[str]] = {
    "test": [
        "pytest",
        "pytest-cov",
        "coverage",
        "toml",
    ],
    "lint": [
        "flake8",
        "isort",
        "black",
        "mypy",
    ],
    "docs": [
        "mkdocs",
        "mkdocs-material",
        "mkdocstrings",
        "markdown-include",
        "livereload",
    ],
    "coverage": [
        "coverage",
        "coverage-badge",
        "toml",
    ],
}

# "dev" should only be run if no virtual environment found and we're not on CI
# i.e. someone is using nox to set up their local dev environment
# to work on {{cookiecutter.project_slug}}
if not VENV_DIR.exists() and not ON_CI:
    nox.options.sessions = ["dev"]
else:
    nox.options.sessions = ["test", "coverage", "lint", "docs"]


def poetry_install(session: nox.Session, *args: str, **kwargs: Any) -> None:
    """
    Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.

    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock.

    This allows you to manage the
    packages as Poetry development dependencies.

    Args:
        session (nox.Session): The enclosing nox Session.

        args (str): List of packages to install.

        kwargs: Keyword arguments passed to session.install.
    """

    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            "--without-hashes",
            external=True,
            silent=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


def set_up_vscode(session: nox.Session) -> None:
    """
    Helper function that will set VSCode's workspace settings
    to use the auto-created virtual environment and enable
    pytest support.

    If called, this function will only do anything if
    there aren't already VSCode workspace settings defined.

    Args:
        session (nox.Session): The enclosing nox session.
    """

    if not VSCODE_DIR.exists():
        session.log("Setting up VSCode Workspace.")
        VSCODE_DIR.mkdir(parents=True)
        SETTINGS_JSON.touch()

        settings = {
            "python.defaultInterpreterPath": PYTHON,
            "python.testing.pytestEnabled": True,
        }

        with open(SETTINGS_JSON, mode="w", encoding="utf-8") as f:
            json.dump(settings, f, sort_keys=True, indent=4)


def update_seeds(session: nox.Session) -> None:
    """
    Helper function to update the core installation seed packages
    to their latest versions in each session.

    Args:
        session (nox.Session): The enclosing nox session.
    """

    session.install("--upgrade", *SEEDS)


def session_requires(session: nox.Session, tool: str) -> None:
    """
    Helper function that 'tells' the session that it requires
    a particular external `tool`.

    When the function is called from within a session it checks
    if `tool` is installed and available on $PATH.

    If the tool is installed, the function does nothing and the
    session is allowed to continue as normal.

    If the tool is not installed, the session is exited immediately
    and an error is thrown.

    Args:
        session (nox.Session): The enclosing nox session.

        tool (str): Name of the external tool to check for.
    """

    if not bool(shutil.which(tool)):
        session.error(
            f"{tool!r} not installed. Session: {session.name!r} requires {tool!r}."
        )


def get_session_requirements(session: nox.Session) -> List[str]:
    """
    Gets the session requirements from the global
    SESSION_REQUIREMENTS dict based on the session name.

    If it cannot find the requirements, will exit the session
    and log an error.

    Args:
        session (nox.Session): The enclosing nox session.

    Returns:
        List[str]: List of requirements for the session.
    """

    requirements = SESSION_REQUIREMENTS.get(f"{session.name}", [])
    if not requirements:
        session.error(
            f"Requirements for nox session: {session.name!r}, not found in noxfile.py."
        )

    return requirements


@nox.session(python=False)
def dev(session: nox.Session) -> None:
    """
    Sets up a python dev environment for the project if one doesn't already exist.
    """

    # Error out if user does not have poetry installed
    session_requires(session, "poetry")

    # Ensure the poetry venv is created in the project root
    session.run("poetry", "config", "virtualenvs.in-project", "true", external=True)
    session.run("poetry", "install", external=True)

    # Poetry doesn't always install latest pip
    # Here we use the absolute path to the poetry venv's python interpreter
    session.run(PYTHON, "-m", "pip", "install", "--upgrade", *SEEDS, silent=True)

    if bool(shutil.which("code")):
        # Only do this is user has VSCode installed
        set_up_vscode(session)


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """
    Runs the test suite against all supported python versions.
    """

    # Error out if user does not have poetry installed
    session_requires(session, "poetry")

    # We can't use get_session_requirements here because the session
    # is parametrized against different python versions meaning the
    # session name is 'test-{version}'
    requirements = SESSION_REQUIREMENTS.get("test", [])
    if not requirements:
        session.error("Requirements for nox session: 'test', not found in noxfile.py.")

    update_seeds(session)
    # Tests require the package to be installed
    session.run("poetry", "install", "--no-dev", external=True, silent=True)
    poetry_install(session, *requirements)

    session.run("pytest", f"--cov={PROJECT_SRC}", f"{PROJECT_TESTS}/")
    # Notify queues up 'coverage' to run next
    # so 'nox -s test' will run coverage afterwards
    session.notify("coverage")


@nox.session(python=DEFAULT_PYTHON)
def coverage(session: nox.Session) -> None:
    """
    Test coverage analysis.
    """

    # Error out if user does not have poetry installed
    session_requires(session, "poetry")

    requirements = get_session_requirements(session)

    if not COVERAGE_BADGE.exists():
        COVERAGE_BADGE.parent.mkdir(parents=True)
        COVERAGE_BADGE.touch()

    update_seeds(session)
    poetry_install(session, *requirements)

    session.run("coverage", "report", "--show-missing")
    session.run("coverage-badge", "-fo", f"{COVERAGE_BADGE}")


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """
    Formats project with black and isort, then runs flake8 and mypy linting.
    """

    # Error out if user does not have poetry installed
    session_requires(session, "poetry")

    requirements = get_session_requirements(session)

    update_seeds(session)
    poetry_install(session, *requirements)

    # If we're on CI, run in check mode so build fails if formatting isn't correct
    if ON_CI:
        session.run("isort", ".", "--check")
        session.run("black", ".", "--check")
    else:
        # If local, go ahead and fix formatting
        session.run("isort", ".")
        session.run("black", ".")

    session.run("flake8", ".")
    session.run("mypy")


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    """
    Builds the project documentation. Use '-- serve' to see changes live.
    """

    # Error out if user does not have poetry installed
    session_requires(session, "poetry")

    requirements = get_session_requirements(session)

    update_seeds(session)
    poetry_install(session, *requirements)

    if "serve" in session.posargs:
        webbrowser.open(url="http://127.0.0.1:8000/{{cookiecutter.project_slug}}/")
        session.run("mkdocs", "serve")
    else:
        session.run("mkdocs", "build", "--clean")


@nox.session(python=DEFAULT_PYTHON)
def build(session: nox.Session) -> None:
    """
    Builds the package sdist and wheel.
    """

    # Error out if user does not have poetry installed
    session_requires(session, "poetry")

    update_seeds(session)
    session.run("poetry", "install", "--no-dev", external=True, silent=True)

    session.run("poetry", "build", external=True)
