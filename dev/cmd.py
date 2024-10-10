import subprocess
import sys


# cmd_wrapper
def run_command(*args, **kwargs):
    try:
        subprocess.run(*args, **kwargs, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{' '.join(e.cmd)}'\n", f"Failed with exit code {e.returncode}")
        sys.exit(1)

def install() -> None:
    print("> install")
    run_command(["poetry", "install"])

def update() -> None:
    print("> update")
    run_command(["poetry", "run", "scripts.update_dependencies:main"])

def test() -> None:
    print("> test")
    run_command(["pytest"])


def refresh() -> None:
    print("> refresh")
    run_command(["poetry", "lock"])
    install()
    run_command(["poetry", "build"])


def typecheck() -> None:
    print("> typecheck")
    run_command(["mypy", "."])


# lint / formatting


def lint() -> None:
    print("> lint")
    run_command(["ruff", "check"])


def lintF() -> None:
    print("> lintF")
    run_command(["ruff", "check", "--fix"])


# sort imports + lint
def format() -> None:
    print("> format")
    run_command(["ruff", "check", "--select", "I", "--fix"])
    run_command(["ruff", "format"])
