import logging
import os
import shutil
import subprocess

import typer
from rich.console import Console
console = Console()
app = typer.Typer(rich_markup_mode="markdown")

import questionary
from src.repositories.main import get_repositories
from src.utils.helpers import Logger

Logger.create_logger(f"{__name__}.log", __package__, False)
logger = logging.getLogger(__name__)

def check_repo_exist(repo_path: str = '.') -> bool:
    """Check if a Git repository exists at the given path."""
    git_dir = os.path.join(repo_path, '.git')
    if os.path.isdir(git_dir):
        logger.debug(f"Repo exists at {repo_path}")
        return True
    else:
        logger.debug(f"No Git repository found at {repo_path}")
        return False

def handle_subprocess_error(e: subprocess.CalledProcessError, message: str) -> None:
    """Handle subprocess errors."""
    logger.error(f"{message}: {str(e)}")
    console.print(f"[bold red]{message}: {str(e)}[/bold red]")

def remove_existing_repo(relative_path: str) -> bool:
    """Remove an existing Git repository at the given path."""
    try:
        # Save the absolute path that points to relative_path
        repo_destination = os.path.abspath(relative_path)

        # Validate the path
        if not os.path.exists(repo_destination):
            logger.error(f"Repository destination does not exist: {repo_destination}")
            console.print(f"[bold red]Repository destination does not exist: {repo_destination}[/bold red]")
            return False

        # Remove contents of repo_destination path
        for filename in os.listdir(repo_destination):
            file_path = os.path.join(repo_destination, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f"Failed to delete {file_path}. Reason: {str(e)}")
                console.print(f"[bold red]Failed to delete {file_path}. Reason: {str(e)}[/bold red]")
                return False

        console.print(f"[bold green]Existing repository at {repo_destination} removed.[/bold green]")
        return True
    except Exception as e:
        handle_subprocess_error(e, "Error removing existing repository")
        return False

def clone_repo(repo_url: str, repo_path: str = '.') -> None:
    """Clone a repository from the given URL to the specified path."""
    if check_repo_exist(repo_path):
        console.print(f"[bold yellow]A Git repository already exists at {repo_path}.[/bold yellow]")
        overwrite = questionary.confirm("Do you want to overwrite it?").ask()
        if not overwrite:
            console.print("[bold red]Cloning aborted.[/bold red]")
            return

        if not remove_existing_repo(repo_path):
            return

    result = subprocess.run(['git', 'clone', repo_url, repo_path], capture_output=True, text=True)
    if result.returncode == 0:
        console.print("[bold green]--- Success ---[/bold green]")
        console.print(result.stdout)
        console.print(f"[bold green]Repository cloned successfully to {repo_path}.[/bold green]")
    else:
        console.print("[bold red]--- Error ---[/bold red]")
        error_message = f"Failed to clone repository:\n{result.stderr}"
        logger.error(error_message)
        console.print(f"[bold red]{error_message}[/bold red]")

def get_template_repositories() -> list:
    """Get the list of template repositories."""
    repo_list = get_repositories().repositories
    logger.debug(f"Template repositories: {repo_list}")
    return repo_list

def select_repository() -> str:
    """Spawn git projects from templates by selecting a repository."""
    print("Selecting repository...")
    try:
        repo_list = get_template_repositories()

        if not repo_list:
            console.print("[bold red]No template repositories available.[/bold red]")
            return None

        # Create a mapping from display titles to actual repository URLs
        choice_map = {f'{repo["name"]} - {repo["url"]}': repo["url"] for repo in repo_list}

        # Add the "Exit" option
        choices = list(choice_map.keys()) + ["Exit"]

        # Use questionary to select a repository
        selected_title = questionary.select(
            "Choose a preset (or 'Exit' to quit):",
            choices=choices,
        ).ask()

        if selected_title == "Exit":
            console.print("[bold yellow]Exiting...[/bold yellow]")
            return None

        # Return the actual repository URL
        selected_repository = choice_map[selected_title]
        logger.debug(f"Selected repository: {selected_repository}")
        return selected_repository

    except Exception as e:
        handle_subprocess_error(e, "Error in spawn command")
        raise typer.Exit(code=1) from e
