# Contributing to {{cookiecutter.project_name}}

I've tried to structure {{cookiecutter.project_name}} to make it nice and easy for people to contribute. Here's how to go about doing it! :smiley:

## Developing

If you want to fix a bug, improve the docs, add tests, add a feature or any other type of direct contribution to {{cookiecutter.project_name}}: here's how you do it!

**To work on {{cookiecutter.project_name}} you'll need python >=3.7**

### Step 1: Fork {{cookiecutter.project_name}}

The first thing to do is 'fork' {{cookiecutter.project_name}}. This will put a version of it on your GitHub page. This means you can change that fork all you want and the actual version of {{cookiecutter.project_name}} still works!

To create a fork, go to the {{cookiecutter.project_name}} [repo] and click on the fork button!

### Step 2: Clone your fork

Navigate to where you do your development work on your machine and open a terminal

**If you use HTTPS:**

```shell
git clone https://github.com/<your_github_username>/{{cookiecutter.project_name}}.git
```

**If you use SSH:**

```shell
git clone git@github.com:<your_github_username>/{{cookiecutter.project_name}}.git
```

**Or you can be really fancy and use the [GH CLI]**

```shell
gh repo clone <your_github_username>/{{cookiecutter.project_name}}
```

HTTPS is probably the one most people use!

Once you've cloned the project, cd into it...

```shell
cd {{cookiecutter.project_name}}
```

This will take you into the root directory of the project.

Now add the original {{cookiecutter.project_name}} repo as an upstream in your forked project:

```shell
git remote add upstream https://github.com/{{cookiecutter.author_github_username}}/{{cookiecutter.project_name}}.git
```

This makes the original version of {{cookiecutter.project_name}} 'upstream' but not 'origin'. Basically, this means that if your working on it for a while and the original project has changed in the meantime, you can do:

```shell
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

This will (in order):

* Checkout the main branch of your locally cloned fork
* Fetch any changes from the original project that have happened since you forked it
* Merge those changes in with what you have
* Push those changes up to your fork so your fork stays up to date with the original.

*Good practice is to do this before you start doing anything every time you start work, then the chances of you getting conflicting commits later on is much lower!*

### Step 3: Create the Environment

#### Install poetry

{{cookiecutter.project_slug}} uses [poetry] as a build tool, in order to work on the project, you'll need to get it too!

I would recommend using [pipx] as this will install [poetry] inside it's own isolated environment and expose the CLI everywhere (the safest way)

``` shell
pipx install poetry
```

Or if you don't want this, you can simply create a virtual environment and install poetry into that, like this:

Create the environment...

``` shell
python3 -m venv .venv
```

Activate it...

=== "macOS & Linux"

    ```shell
    source .venv/bin/activate
    ```

=== "Windows"

    ```shell
    .\.venv.\Scripts.\Activate.ps1
    ```

Then just install [poetry] like any other package...

``` shell
pip install poetry
```

#### Create the Dev Environment

Now you have [poetry] you can get to work!

Just run...

```shell
poetry install
```

And now your environment should be set up, {{cookiecutter.project_name}} should be installed along with everything you need to develop on it :thumbsup:

!!! note

    Under the hood poetry just uses the normal virtual environment stuff you might be used to. So once it's created it for you, you can activate it as normal! By default poetry keeps it's virtual environments in a seperate folder, but I would recommend keeping them in your project folder as this is a bit cleaner and makes it obvious which virtual environment goes with which project!

    To do this just run `poetry config virtualenvs.in-project true` beforehand.

### Step 5: Do your thing

**Always checkout a new branch before changing anything**

```shell
git checkout -b <name-of-your-bugfix-or-feature>
```

Now you're ready to start working!

*Remember! {{cookiecutter.project_name}} aims for high test coverage. If you implement a new feature, make sure to write tests for it! Similarly, if you fix a bug, it's good practice to write a test that would have caught that bug so we can be sure it doesn't reappear in the future!*

{{cookiecutter.project_name}} uses [nox] for automated testing, building the docs, formatting and linting etc. So when you've made your changes, just run:

```shell
nox
```

And it will tell you if something's wrong!

### Step 6: Commit your changes

Once you're happy with what you've done, add the files you've changed:

```shell
git add <changed-file(s)>

# Might be easier to do
git add -A

# But be wary of this and check what it's added is what you wanted..
git status
```

Commit your changes:

```shell
git commit

# Now write a good commit message explaining what you've done and why.
```

While you were working on your changes, the original project might have changed (due to other people working on it). So first, you should rebase your current branch from the upstream destination. Doing this means that when you do your PR, it's all compatible:

```shell
git pull --rebase upstream main
```

Now push your changes to your fork:

```shell
git push origin <your-branch-name>
```

### Step 7: Create a Pull Request

Now go to the original {{cookiecutter.project_name}} [repo] and create a Pull Request. Make sure to choose upstream repo "main" as the destination branch and your forked repo "your-branch-name" as the source.

Thats it! Your code will be tested automatically by {{cookiecutter.project_name}}'s CI suite and if everything passes and your PR is approved and merged then it will become part of {{cookiecutter.project_name}}!

*Note: There is a good guide to open source contribution workflow [here] and also [here too]*

## Contributing to Docs

Any improvements to the documentation are always appreciated! {{cookiecutter.project_name}} uses [mkdocs] with the [mkdocs-material] theme so the documentation is all written in markdown and can be found in the `docs` folder in the project root.

Because {{cookiecutter.project_name}} uses [nox], things like building and serving the documentation is super easy. All you have to do is:

```shell
# Builds the docs
nox -s docs

# Or again, the makefile
make docs

# If you want to work on the docs and have them live-reload on changes...
make autodocs
```

If you add pages to the docs, make sure they are placed in the nav tree in the `mkdocs.yml` file and you're good to go!

[GH CLI]: https://cli.github.com
[nox]: https://nox.thea.codes/en/stable/
[repo]: https://github.com/{{cookiecutter.author_github_username}}/{{cookiecutter.project_name}}
[here]: https://stackoverflow.com/questions/20956154/whats-the-workflow-to-contribute-to-an-open-source-project-using-git-pull-reque
[here too]: https://github.com/asmeurer/git-workflow
[mkdocs]: https://www.mkdocs.org
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[poetry]: https://poetry.readthedocs.io/en/latest/index.html
[pipx]: https://pypa.github.io/pipx/
