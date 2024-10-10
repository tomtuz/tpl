import subprocess
import sys
import tempfile

from src.utils.helpers import validate_repo_url


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


def plugin_eslint(repo_url, repo_dir):
    if not validate_repo_url(repo_url):
        print(f"Invalid repository URL: {repo_url}")
        print("Please provide a valid HTTP or HTTPS URL.")
        sys.exit(1)

    corepack_installed = check_command_installed("corepack")
    pnpm_installed = check_command_installed("pnpm")

    if not corepack_installed and not pnpm_installed:
        print("Error: Neither corepack nor pnpm is installed or in the system PATH.")
        print("Please install either corepack or pnpm and ensure it's in your system PATH before running this command.")
        sys.exit(1)

    package_manager = "pnpm" if pnpm_installed else "npm"

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
            subprocess.run([package_manager, "install"], cwd=temp_dir, check=True)
            subprocess.run([package_manager, "run", "build"], cwd=temp_dir, check=True)

            link_command = (
                [package_manager, "link", "--global"] if package_manager == "pnpm" else [package_manager, "link"]
            )
            subprocess.run(link_command, cwd=temp_dir, check=True)

            print(f"ESLint config from {repo_url} has been installed and linked globally using {package_manager}.")
        except subprocess.CalledProcessError as e:
            print(f"Error during ESLint config installation: {e}")
            print(f"Command output: {e.output.decode() if e.output else 'No output'}")
            print(f"Error output: {e.stderr.decode() if e.stderr else 'No error output'}")
            sys.exit(1)
