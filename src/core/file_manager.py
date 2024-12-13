import os
import platform
import shutil

from src.utils.helpers import Logger

logger = Logger.create_logger(f"{__name__}.log", __package__, False)


def get_config_dir():
    """Get the configuration directory path based on the operating system."""
    if platform.system() == "Windows":
        config_dir = os.path.join(os.environ.get("USERPROFILE"), ".config", "tpl")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "tpl")
    logger.debug(f"Configuration directory: {config_dir}")
    return config_dir


def get_repos_dir():
    """Get the repositories directory path."""
    repos_dir = os.path.join(get_config_dir(), "repos")
    logger.debug(f"Repositories directory: {repos_dir}")
    return repos_dir


def ensure_dir(directory):
    """Ensure the directory exists, creating it if necessary."""
    try:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")
    except Exception as e:
        logger.error(f"Failed to ensure directory {directory}. Reason: {str(e)}")
        logger(f"[bold red]Failed to ensure directory {directory}. Reason: {str(e)}[/bold red]")


def copy_file(src, dest):
    """Copy a file from source to destination."""
    try:
        shutil.copy2(src, dest)
        logger.debug(f"File copied from {src} to {dest}")
        return True
    except Exception as e:
        logger.error(f"Error copying file from {src} to {dest}. Reason: {str(e)}")
        logger(f"[bold red]Error copying file from {src} to {dest}. Reason: {str(e)}[/bold red]")
        return False


def create_project_directory(project_name):
    """Create a project directory with the given name."""
    if platform.system() == "Windows":
        folderPath = os.path.join(os.environ.get("USERPROFILE"), ".config", "tpl", project_name)
    else:
        folderPath = os.path.join(os.path.expanduser("~"), ".config", "tpl", project_name)

    try:
        os.makedirs(folderPath, exist_ok=True)
        logger.debug(f"Project directory created: {folderPath}")
        return folderPath
    except Exception as e:
        logger.error(f"Error creating project directory {folderPath}. Reason: {str(e)}")
        logger(f"[bold red]Error creating project directory {folderPath}. Reason: {str(e)}[/bold red]")
        return None


def get_template_path(template_name):
    """Get the path to the template directory."""
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    template_path = os.path.join(template_dir, template_name)
    logger.debug(f"Template path for {template_name}: {template_path}")
    return template_path


def copy_template(template_name, destination):
    """Copy a template directory to the destination."""
    template_path = get_template_path(template_name)
    if not os.path.exists(template_path):
        logger.error(f"Template '{template_name}' not found.")
        logger(f"[bold red]Template '{template_name}' not found.[/bold red]")
        return False

    try:
        shutil.copytree(template_path, destination, dirs_exist_ok=True)
        logger.debug(f"Template {template_name} copied to {destination}")
        return True
    except Exception as e:
        logger.error(f"Error copying template {template_name} to {destination}. Reason: {str(e)}")
        logger(f"[bold red]Error copying template {template_name} to {destination}. Reason: {str(e)}[/bold red]")
        return False


def get_repo_path(repo_name):
    """Get the path to the repository directory."""
    repo_path = os.path.join(get_repos_dir(), repo_name)
    logger.debug(f"Repository path for {repo_name}: {repo_path}")
    return repo_path


def ensure_repo_dir(repo_name):
    """Ensure the repository directory exists, creating it if necessary."""
    repo_path = get_repo_path(repo_name)
    ensure_dir(repo_path)
    return repo_path
