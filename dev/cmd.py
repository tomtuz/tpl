import subprocess


def tpl() -> None:
    subprocess.run(["poetry", "run", "src.cli:run"])

# (name agnostic alias)
def pop() -> None:
    subprocess.run(["poetry", "run", "src.cli:run"])

def install() -> None:
    subprocess.run(["poetry", "install"])

def build() -> None:
    subprocess.run(["poetry", "run", "scripts.build:main"])

def test() -> None:
    subprocess.run(["pytest"])

def refresh() -> None:
    subprocess.run(["poetry", "lock"])
    install()
    build()

def typecheck() -> None:
    subprocess.run(["mypy", "."])

# lint / formatting

def lint() -> None:
    subprocess.run(["ruff", "check"])


def lintF() -> None:
    subprocess.run(["ruff", "check", "--fix"])

# sort imports + lint
def format() -> None:
    subprocess.run(["ruff", "check", "--select", "I", "--fix"])
    subprocess.run(["ruff", "format"])
