from invoke import task


@task
def build(c):
    c.run("python3 scripts/build.py")


@task
def install(c):
    c.run("python3 scripts/dev/cmd.py install")


@task
def test(c):
    c.run("python3 scripts/dev/cmd.py test")


@task
def refresh(c):
    c.run("python3 scripts/dev/cmd.py refresh")


@task
def typecheck(c):
    c.run("python3 scripts/dev/cmd.py typecheck")


@task
def lint(c):
    c.run("python3 scripts/dev/cmd.py lint")


@task
def lintF(c):
    c.run("python3 scripts/dev/cmd.py lintF")


@task
def format(c):
    c.run("python3 scripts/dev/cmd.py format")
