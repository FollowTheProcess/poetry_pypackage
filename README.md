# Poetry Pypackage

![License](https://img.shields.io/github/license/FollowTheProcess/poetry_pypackage.svg)
[![GitHub](https://img.shields.io/github/v/release/FollowTheProcess/poetry_pypackage?logo=github&sort=semver)](https://github.com/FollowTheProcess/poetry_pypackage)
[![CI](https://github.com/FollowTheProcess/poetry_pypackage/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/poetry_pypackage/actions?query=workflow%3ACI)

A modern python package template, inspired by the [original] but with some updates bringing it to the forefront of modern python!

## Changes from the Original

* Changed from [tox] to [nox] for flexible python test automation
* Drop support for unittest in favour of [pytest]
* Change CI provider from Travis to [GitHub actions]
* Change docs from [Sphinx] to [MkDocs]
* Built in support for static type hinting/checking with [mypy]
* Made compliant with PEP 517/518
* Uses [poetry] as a build tool

## Features

### [GitHub Actions]

The project template comes with a ready to go GitHub Actions configuration file which automates all your code quality checks:

* Testing with pytest
* Linting with [flake8], [isort], and [mypy]
* Formatting with [black]

### [Nox]

Easy automation & flexible testing for python 3.7+:

* nox is just like tox, but with easy configuration in a python file
* Comes preconfigured to do project maintainence tasks like build and serve docs in one command:

``` shell
nox docs -- serve
```

### [MkDocs]

Production ready docs with MkDocs and GitHub Pages. Sphinx has been the go to for python documentation but MkDocs offers easier configuration and documentation in markdown.

Project template comes with configured `mkdocs.yml` config file for a beautiful theme, all you need to do is add your markdown files and reference them in your nav tree!

Examples of MkDocs sites include [FastAPI], [Typer], [isort] and more!

When you're ready to deploy your documentation, just run:

``` shell
mkdocs gh-deploy
```

And your docs will be right there next to your code on [GitHub Pages]

### Easy Versioning

Pre-configured version bumping with [Bump2Version], all you need to do when you're ready for a new version is:

``` shell
bump2version patch # Possible: patch, minor, major
git push
git push --tags
```

And your new version will be pushed up in a new commit and tag.

You can also choose to automatically release your new version to [PyPI] if your CI passes by creating a [PyPI API Token] and saving it in a repository secret named `PYPI_API_TOKEN`

* Don't worry, your package will only be uploaded to PyPI if all other CI actions pass (testing, linting, building docs etc.)

### [GitHub CLI]

Option to use the new GitHub CLI to create a GitHub repo for you during project creation. (You'll need to have this already installed)

### PEP 517/518 Ready

PEP 517 & 518 (think `pyproject.toml`) are on their way to becoming the default. No more `requirements.txt` `requirements_dev.txt` `requirements_docs.txt`. We use [poetry] for this now so all you need to do now is:

``` shell
# Installs your project and its dependencies
poetry install
```

### GitHub Issue Labelling

Series of helpful labels that you can use to categorise issues and pull requests. These come in especially handy when combined with the Release Drafter workflow!

### Automatic Release Drafts

Automatically generate release notes with the [Release Drafter] workflow. This uses the labels from issues and pull requests to draft pretty and detailed release notes for your GitHub releases.

This is automatically run when you push a new tag to main.

## Usage

* Ensure you have cookiecutter installed:

``` shell
# Mac
brew install cookiecutter

# Linux
apt-get install cookiecutter

# pipx
pipx install cookiecutter
```

* Navigate to where you keep your projects

* Call cookiecutter with this template and answer all the questions

``` shell
cookiecutter https://github.com/FollowTheProcess/poetry_pypackage.git --checkout v0.2.3
```

* Create a virtual environment, a git repo (if not using the gh cli) and start developing

Either do this yourself:

``` shell
cd <name_of_your_project>

poetry install
```

Or just let [nox] do it!

``` shell
nox
```

* Make a first commit to set up the github repo (if you didn't use the gh cli)

* That should be it! from now on everything will be handled automatically. All you need to do is write code, tests and docs! Your code will be style checked, your tests will be run etc.

[original]: https://github.com/audreyfeldroy/cookiecutter-pypackage
[tox]: https://tox.readthedocs.io/en/latest/
[nox]: https://nox.thea.codes/en/stable/
[pytest]: https://docs.pytest.org/en/stable/
[GitHub actions]: https://docs.github.com/en/free-pro-team@latest/actions
[Sphinx]: https://www.sphinx-doc.org/en/master/
[MkDocs]: https://www.mkdocs.org
[Bump2Version]: https://pypi.org/project/bump2version/
[GitHub CLI]: https://cli.github.com
[PyPI]: https://pypi.org
[flake8]: https://flake8.pycqa.org/en/latest/
[isort]: https://pycqa.github.io/isort/
[black]: https://black.readthedocs.io/en/stable/
[mypy]: https://mypy.readthedocs.io/en/stable/
[FastAPI]: https://fastapi.tiangolo.com
[Typer]: https://typer.tiangolo.com
[GitHub Pages]: https://pages.github.com
[PyPI API Token]: https://pypi.org/help/#apitoken
[poetry]: https://python-poetry.org
