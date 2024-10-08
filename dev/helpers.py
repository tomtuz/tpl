import subprocess

def install() -> None:
    subprocess.run(["poetry", "install"])


def test() -> None:
    subprocess.run(["pytest"])


def lint() -> None:
    subprocess.run(["ruff", "check"])


def lintF() -> None:
    subprocess.run(["ruff", "check", "--fix"])


def typecheck() -> None:
    subprocess.run(["mypy", "."])


# sort imports + lint
def format() -> None:
    subprocess.run(["ruff", "check", "--select", "I", "--fix"])
    subprocess.run(["ruff", "format"])
