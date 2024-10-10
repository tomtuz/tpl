import click

from src import main


@click.group()
def cli() -> None:
    print("> src.cli.cli")
    """Default CLI"""
    pass

@cli.command()
@click.argument("args", nargs=-1)
def config(args):
    print("> sc.cli.config")
    """Run the config command with arguments"""
    main(command="config", args=list(args))


@cli.command()
@click.argument("args", nargs=-1)
def spawn(args):
    """Run the spawn command with arguments"""
    print("> src.cli.spawn")
    main(command="spawn", args=list(args))


@cli.command()
@click.argument("args", nargs=-1)
def template(args):
    """Run the template command with arguments"""
    print("> src.cli.template")
    main(command="template", args=list(args))


@cli.command()
@click.argument("args", nargs=-1)
def plugin(args):
    """Run the plugin command with arguments"""
    print("> src.cli.plugin")
    main(command="plugin", args=list(args))


if __name__ == "__main__":
    cli()
