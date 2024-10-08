import click
from typing import Optional

from src.main import main
# from src.core.plugin_loader import load_plugins, list_plugins, get_plugin

@click.group()
def cli() -> None:
    """Default CLI"""
    pass

@cli.command()
def dev() -> None:
    """Run the main() functionality"""
    main()

@cli.command()
def other() -> None:
    """Run other command"""
    click.echo("Running other...")

@cli.command()
@click.argument('args', nargs=-1)
def spawn(args):
    """Run the spawn command with arguments"""
    main(command='spawn', args=args)

@cli.command()
@click.argument('args', nargs=-1)
def template(args):
    """Run the template command with arguments"""
    main(command='template', args=args)

@cli.command()
@click.argument('args', nargs=-1)
def plugin(args):
    """Run the plugin command with arguments"""
    main(command='plugin', args=args)

def run() -> None:
    cli()
