#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile

from urllib.parse import urlparse

from definitions import ROOT_DIR

from src.core import file_manager


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


def get_project_root():
    return ROOT_DIR


def get_file_index_path():
    print(f"[DEBUG] __package__: {__package__}")
    print(f"[DEBUG] __file__: {__file__}")
    if getattr(sys, "frozen", False):
        # The application is frozen (packaged)
        base_path = sys._MEIPASS
        print(f"[DEBUG] Application is frozen. Base path: {base_path}")
    else:
        base_path = get_project_root()
        print(f"[DEBUG] Running from source. Base path: {base_path}")

    file_index_path = os.path.join(base_path, "src", "file_index")
    print(f"[DEBUG] Final file_index_path: {file_index_path}")
    return file_index_path


def validate_repo_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc


def check_command_installed(command):
    try:
        subprocess.run(
            [command, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {command}: {e}")
        print(f"Output: {e.output.decode()}")
        print(f"Error: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print(f"{command} not found in PATH")
        return False


def getFile(filename, variant="base", target_dir=os.getcwd()):
    print(
        f"[DEBUG] getFile called with: filename={filename}, variant={variant}, target_dir={target_dir}"
    )

    file_index_path = get_file_index_path()
    print(f"[DEBUG] file_index_path: {file_index_path}")

    source_file = os.path.join(file_index_path, filename, f"{variant}.json")
    print(f"[DEBUG] Constructed source_file: {source_file}")

    print(f'"source": {source_file}')
    print(f'"target": {target_dir}')

    if not os.path.exists(source_file):
        print(f"[FAIL] '{filename}' file index doesn't exist.")
        print(f"[DEBUG] Checked path: {source_file}")
        return 1

    target_file = os.path.join(target_dir, f"{filename}_{variant}.json")
    print(f"[DEBUG] Constructed target_file: {target_file}")

    if file_manager.copy_file(source_file, target_file):
        print(f"[OK] Copied '{filename}' index to {target_file}")
        return 0
    else:
        print(f"[FAIL] to copy '{filename}' index")
        print(f"[DEBUG] Copy failed from {source_file} to {target_file}")
        return 1


def print_all_indexes(directory):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    # Get all items in the directory
    items = os.listdir(directory)

    # Filter and print only the folders
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]

    if folders:
        print("\nAll folders in 'src/file_index':")
        for folder in folders:
            print(f"- {folder}")
    else:
        print(f"No folders found in '{directory}'.")


def plugin_eslint(repo_url, repo_dir):
    if not validate_repo_url(repo_url):
        print(f"Invalid repository URL: {repo_url}")
        print("Please provide a valid HTTP or HTTPS URL.")
        sys.exit(1)

    corepack_installed = check_command_installed("corepack")
    pnpm_installed = check_command_installed("pnpm")

    if not corepack_installed and not pnpm_installed:
        print("Error: Neither corepack nor pnpm is installed or in the system PATH.")
        print(
            "Please install either corepack or pnpm and ensure it's in your system PATH before running this command."
        )
        sys.exit(1)

    package_manager = "pnpm" if pnpm_installed else "npm"

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone the repository
            subprocess.run(["git", "clone", repo_url, temp_dir], check=True)

            # Install dependencies
            subprocess.run([package_manager, "install"], cwd=temp_dir, check=True)

            # Build the project
            subprocess.run([package_manager, "run", "build"], cwd=temp_dir, check=True)

            # Link the package globally
            link_command = (
                [package_manager, "link", "--global"]
                if package_manager == "pnpm"
                else [package_manager, "link"]
            )
            subprocess.run(link_command, cwd=temp_dir, check=True)

            print(
                f"ESLint config from {repo_url} has been installed and linked globally using {package_manager}."
            )
        except subprocess.CalledProcessError as e:
            print(f"Error during ESLint config installation: {e}")
            print(f"Command output: {e.output.decode() if e.output else 'No output'}")
            print(
                f"Error output: {e.stderr.decode() if e.stderr else 'No error output'}"
            )
            sys.exit(1)
