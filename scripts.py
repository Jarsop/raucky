"""
Scripts helper for poetry run subcommands
"""

import subprocess

MODULES = ["raucky.py", "raucky_lib", "scripts.py", "tests"]


def fmt():
    """
    Run black. Equivalent to:
    `poetry run python -u -m black ${MODULES}`
    """
    print("\n=> Black:")
    subprocess.run(["python", "-u", "-m", "black", *MODULES], check=True)


def lint():
    """
    Run black. Equivalent to:
    `poetry run python -u -m mypy ${MODULES}`
    and:
    `poetry run python -u -m pylint ${MODULES}`
    """
    print("\n=> MyPy:")
    subprocess.run(["python", "-u", "-m", "mypy", *MODULES], check=True)
    print("\n=> Pylint:")
    subprocess.run(["python", "-u", "-m", "pylint", *MODULES], check=True)


def test():
    """
    Run all pytests. Equivalent to:
    `poetry run python -u -m pytest -vv`
    """
    print("\n=> Pytest:")
    subprocess.run(["python", "-u", "-m", "pytest", "-vv"], check=True)


def all():  # pylint: disable=redefined-builtin
    """
    Run all commands in this script
    """
    fmt()
    lint()
    test()
