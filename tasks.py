import os
import sys

from invoke import task, util


in_ci = os.environ.get("CI", "false") == "true"
if in_ci:
    pty = False
else:
    pty = util.isatty(sys.stdout) and util.isatty(sys.stderr)


@task
def reformat(c):
    c.run("isort mopidy_webhooks tests setup.py tasks.py", pty=pty)
    c.run("black mopidy_webhooks tests setup.py tasks.py", pty=pty)


@task
def lint(c):
    c.run(
        "flake8 --show-source --statistics --max-line-length 100 mopidy_webhooks tests",
        pty=pty,
    )
    c.run("check-manifest", pty=pty)


@task
def test(c, onefile=""):
    pytest_args = [
        "pytest",
        "--strict-config",
        "--cov=mopidy_webhooks",
        "--cov-report=term-missing",
    ]
    if in_ci:
        pytest_args.extend(("--cov-report=xml", "--strict-markers"))
    else:
        pytest_args.append("--cov-report=html")

    if onefile:
        pytest_args.append(onefile)

    c.run(" ".join(pytest_args), pty=pty)


@task
def type_check(c):
    c.run("mypy mopidy_webhooks tests", pty=pty)
