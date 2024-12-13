#!/usr/bin/env python3

import logging
from typing import Optional

import typer
from rich.console import Console

from src.cli_selector.file import cli_selector_spawn
from src.core.commands import cmd_config, cmd_plugin, cmd_repository, cmd_spawn, cmd_template
from src.core.plugin_loader import load_plugins
from src.utils.helpers import Logger

app = typer.Typer(rich_markup_mode="markdown")
console = Console()

Logger.create_logger(f"{__name__}.log", __package__, False)
logger = logging.getLogger(__name__)


@app.command()
def config(
    action: str = typer.Argument(..., help="Action to perform: get, set, remove, or list"),
    key: Optional[str] = typer.Argument(None, help="Configuration key (not required for 'list' action)"),
    value: Optional[str] = typer.Argument(None, help="Value to set (only for 'set' action)"),
):
    """Manage configuration settings for the TPL tool."""
    logger.info(f"config command called with action: {action}, key: {key}, value: {value}")
    try:
        args = [action]
        if key:
            args.append(key)
        if value:
            args.append(value)
        cmd_config(args)
    except Exception as e:
        logger.error(f"Error in config command: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e


@app.command()
def spawn(
    filename: Optional[str] = typer.Argument(None, help="Filename to spawn"),
    variant: Optional[str] = typer.Argument(None, help="Variant of the file to spawn"),
):
    """Spawn new files or projects from templates."""
    logger.info(f"spawn command called with filename: {filename}, variant: {variant}")
    try:
        if filename is None:
            cli_selector_spawn()
        else:
            args = [arg for arg in [filename, variant] if arg is not None]
            cmd_spawn(args)
    except Exception as e:
        logger.error(f"Error in spawn command: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e


@app.command()
def template(
    template_name: str = typer.Argument(..., help="Name of the template"),
    command: str = typer.Argument(..., help="Command to run on the template"),
    options: Optional[list[str]] = typer.Argument(None, help="Additional options for the template command"),
):
    """Manage and use templates for file generation."""
    logger.info(f"template command called with template_name: {template_name}, command: {command}, options: {options}")
    try:
        args = [template_name, command] + (options or [])
        cmd_template(args)
    except Exception as e:
        logger.error(f"Error in template command: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e


@app.command()
def plugin(
    plugin_name: Optional[str] = typer.Argument(None, help="Name of the plugin to run"),
    options: Optional[list[str]] = typer.Argument(None, help="Additional options for the plugin"),
):
    """Manage and use plugins to extend TPL functionality."""
    logger.info(f"plugin command called with plugin_name: {plugin_name}, options: {options}")
    try:
        args = [plugin_name] + (options or []) if plugin_name else []
        cmd_plugin(args)
    except Exception as e:
        logger.error(f"Error in plugin command: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e


@app.command()
def repository():
    """Use repository templates"""
    try:
        cmd_repository()
    except Exception as e:
        logger.error(f"Error in repository command: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e


def version_callback(value: bool):
    if value:
        console.print("TPL version 0.1.0")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True, help="Show the version and exit."
    ),
):
    """
    TPL - Template and Script Runner CLI

    A versatile tool for managing project templates, configurations, and plugins.
    """
    logger.info("Main callback called")
    load_plugins()
    if ctx.invoked_subcommand is None:
        logger.info("No subcommand was used. Showing help message.")
        console.print(ctx.get_help())
        raise typer.Exit(code=0)


if __name__ == "__main__":
    try:
        logger.debug("Starting application")
        app()
    except SystemExit as e:
        logger.info(f"Application exited with code: {e.code}")
        raise
    except Exception as e:
        logger.error(f"An unhandled error occurred: {str(e)}")
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e
