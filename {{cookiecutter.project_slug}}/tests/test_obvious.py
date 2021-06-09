from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import hello


def test_silly_placeholder():
    """
    Test for silly placeholder in
    {{cookiecutter.project_slug}}.py
    """

    want = "Hello {{cookiecutter.project_slug}}"
    got = hello()

    assert got == want
