"""
Tests for poetry_pypackage.

Author: Tom Fleet
Created: 09/07/2021
"""

import datetime
from pathlib import Path

fake_project = {
    "project_name": "My Test Project",
    "project_short_description": "Testy test test.",
    "author_github_username": "Me",
    "author_name": "Its me",
    "author_email": "itsme@gmail.com",
    "use_gh_cli_to_create_repo": "n",
}


def test_bake_project(cookies):
    result = cookies.bake(extra_context=fake_project)

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "my_test_project"
    assert result.project_path.is_dir()


def test_year_in_generated_license(cookies):

    result = cookies.bake(extra_context=fake_project)

    license_file_path: Path = result.project_path.joinpath("LICENSE")
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read_text()


def test_author_name_in_generated_license(cookies):

    result = cookies.bake(extra_context=fake_project)

    license_file_path: Path = result.project_path.joinpath("LICENSE")
    assert fake_project.get("author_name") in license_file_path.read_text()


def test_bake_produces_correct_files(cookies):

    result = cookies.bake(extra_context=fake_project)

    assert result.project_path.is_dir()
    assert result.exit_code == 0
    assert result.exception is None

    found_toplevel_files = [f.name for f in result.project_path.iterdir()]
    assert "pyproject.toml" in found_toplevel_files
    assert "noxfile.py" in found_toplevel_files
    assert "CHANGELOG.md" in found_toplevel_files


def test_no_template_syntax_in_generated_project(cookies):

    result = cookies.bake(extra_context=fake_project)

    python_files = [f for f in result.project_path.rglob("*.py")]
    yml_files = [f for f in result.project_path.rglob("*.yml")]
    md_files = [f for f in result.project_path.rglob("*.md")]
    toml_files = [f for f in result.project_path.rglob("*.toml")]

    generated_files = python_files + yml_files + md_files + toml_files

    for file in generated_files:
        text = file.read_text()
        assert "{{cookiecutter.project_name}}" not in text
        assert "{{cookiecutter.project_slug}}" not in text
        assert "{{cookiecutter.project_short_description}}" not in text
        assert "{{cookiecutter.open_source_license}}" not in text
        assert "{{cookiecutter.author_github_username}}" not in text
        assert "{{cookiecutter.project_github_url}}" not in text
        assert "{{cookiecutter.author_name}}" not in text
        assert "{{cookiecutter.author_email}}" not in text
