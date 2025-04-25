import os

import nox
from nox_poetry import session

python_versions = ["3.12", "3.13"]

locations = "src", "tests", "examples", "noxfile.py"

package = "interpolation_lib"

nox.options.sessions = ["formatter", "linter", "mypy", "pytype", "tests"]

REQUIREMENTS_FILE_DEV = "temp_dev_requirements.txt"


@session(python=python_versions)
def formatter(session):
    """Проверить код с помощью Ruff."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)


@session(python=python_versions)
def linter(session):
    """Проверить код с помощью Ruff."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", *args)


@session(python=python_versions)
def mypy(session):
    """Запустить проверку типов mypy."""
    session.install("mypy")
    session.run("mypy", "--ignore-missing-imports", *locations)


@session(python=python_versions)
def pytype(session):
    """Запустить статический анализатор pytype."""
    session.install("pytype")
    session.run("pytype", *locations)


@session(python=python_versions)
def tests(session):
    """Запустить тесты с помощью Pytest и проверить покрытие."""
    args = session.posargs or ["-v"]
    session.run_always(
        "poetry",
        "export",
        "--with",
        "dev",
        "--without-hashes",
        "--format",
        "requirements.txt",
        f"--output={REQUIREMENTS_FILE_DEV}",
        external=True,
    )

    session.install(f"-r{REQUIREMENTS_FILE_DEV}")

    session.run(
        "pip",
        "install",
        "-e",
        ".",
        external=True,
    )

    session.run(
        "pytest",
        f"--cov=src/{package}",
        "--cov-report=term-missing",
        "--cov-report=html",
        *args,
    )
    if os.path.exists(REQUIREMENTS_FILE_DEV):
        os.remove(REQUIREMENTS_FILE_DEV)
        session.log(f"Removed {REQUIREMENTS_FILE_DEV}")
