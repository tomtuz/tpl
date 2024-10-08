import sys
import os
import subprocess
from src.core import file_manager
from src.core import utils 

# Goal: Setup ESLint package. Build the package. Link the package package globally.
# 1. Set up test repo 'test-package'
#  - get path of 'test-package' repo: 'config' dir + 'test-package'
#  - ensure dir (create or not)

# 2. Copy a file: 'source' to 'target'. Validate.
# 3. Get 'poetry' template path.
# 4. Copied 'poetry_template'.
# 5. Clean up

def install_eslint_config(repo_dir, repo_url):
    print("Install ESLint Config:", repo_dir)

    repoPath = file_manager.ensure_repo_dir(repo_dir)
    print(f"Created folder: {repoPath}")

    corepack_installed = utils.check_command_installed('corepack')

    npm_installed = utils.check_command_installed('npm')
    pnpm_installed = utils.check_command_installed('pnpm')
    yarn_installed = utils.check_command_installed('yarn')

    print("Sort out package managers")
    package_manager = None
    if pnpm_installed:
        package_manager = 'pnpm'
    elif npm_installed:
        package_manager = 'npm'
    elif yarn_installed:
        package_manager = 'yarn'
    else:
      print("'undefined' package manager")
      sys.exit(1)
      return

    print("Selected package manager: ", package_manager)

    # install dependencies
    if corepack_installed:
      subprocess.run(['corepack', 'use', repo_dir, repo_dir], check=True)
      return

    if not corepack_installed and not pnpm_installed:
      print("Error: Neither corepack nor pnpm is installed or in the system PATH.")
      print("Please install either corepack or pnpm and ensure it's in your system PATH before running this command.")
      sys.exit(1)

    try:
        # Clone the repository
        print(f"git clone {repo_url} {repo_dir}")
        subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)

        # Install dependencies
        print("Installing dependencies...")
        subprocess.run([package_manager, 'install'], cwd=repo_dir, check=True)

        # Build the project
        print("Building the project...")
        subprocess.run([package_manager, 'run', 'build'], cwd=repo_dir, check=True)

        # Link the package globally
        print("Linking package globally...")
        subprocess.run([package_manager, 'link', '--global'], cwd=repo_dir, check=True)

        print(f"ESLint config from {repo_dir} has been installed and linked globally.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during ESLint config installation: {e}")
        return False

def validate_installation(repo_dir):
    # Check if package.json exists
    if not os.path.exists(os.path.join(repo_dir, 'package.json')):
        print("Error: package.json not found in the installed repository.")
        return False

    # Check if the package is globally linked
    try:
        result = subprocess.run(['pnpm', 'list', '-g'], capture_output=True, text=True, check=True)
        if os.path.basename(repo_dir) not in result.stdout:
            print("Error: Package is not globally linked.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking global links: {e}")
        return False

    return True

def run(dir, url):
    print('RUN()')
    # if len(args) < 1:
    #     print("Usage: tpl eslint_config <repo_url>")
    #     return

    # repo_url, repo_dir = args
    print("run repo:", url)
    print("run dir:", dir)

    if install_eslint_config(dir, url):
      print('finished installing')
        # repo_name = os.path.basename(repo_url).replace('.git', '')
        # repo_dir = file_manager.get_repo_path(repo_name)
        
    #     if validate_installation(repo_dir):
    #         config_manager.set_config_value('eslint.main', repo_url)
    #         print(f"ESLint config URL saved: {repo_url}")
            
    #         # Verify the config was saved
    #         saved_url = config_manager.get_config_value('eslint.main')
    #         print(f"Verified saved URL: {saved_url}")
    #     else:
    #         print("Failed to validate ESLint config installation.")
    # else:
    #     print("Failed to install ESLint config.")

def register_plugin():
    return {
        "name": "eslint_config",
        "description": "Install and manage ESLint configurations",
        "run": run
    }
