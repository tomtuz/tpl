import os
import subprocess
import sys

from src.core.config_manager import get_config_value
from src.core.config_manager import set_config_value


def check_poetry_installed():
    try:
        subprocess.run(
            ["poetry", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except FileNotFoundError:
        return False


def create_poetry_project(project_name):
    if not check_poetry_installed():
        print("Poetry is not installed. Please install Poetry and try again.")
        print(
            "Visit https://python-poetry.org/docs/#installation for installation instructions."
        )
        sys.exit(1)

    try:
        # Get the default Python version from configuration, or use a default value
        python_version = get_config_value("default_python_version", "3.9")

        subprocess.run(["poetry", "new", project_name], check=True)
        os.chdir(project_name)

        # Use the configured Python version
        subprocess.run(["poetry", "env", "use", python_version], check=True)
        subprocess.run(["poetry", "install"], check=True)

        print(
            f"Poetry project '{project_name}' has been created with Python {python_version} and dependencies installed."
        )

        # Save the last created project name in the configuration
        set_config_value("last_created_project", project_name)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the Poetry project: {e}")
        sys.exit(1)


def run(args):
    if len(args) < 1:
        print("Usage: tpl poetry new <project_name>")
        sys.exit(1)

    project_name = args[0]
    create_poetry_project(project_name)


if __name__ == "__main__":
    run(sys.argv[1:])
