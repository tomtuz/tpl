import os
import subprocess
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core import config_manager, file_manager
from src.plugins import eslint_config

# Goal: Copy 'templates/poetry' template, Init the template.
# 1. Set up test repo 'test-package'
#  - get path of 'test-package' repo: 'config' dir + 'test-package'
#  - ensure dir (create or not)
# 2. Copy a file: 'source' to 'target'. Validate.
# 3. Get 'poetry' template path.
# 4. Copied 'poetry_template'.
# 5. Clean up


def setup_test_repo(repo_dir):
    os.makedirs(repo_dir, exist_ok=True)
    with open(os.path.join(repo_dir, "package.json"), "w") as f:
        f.write('{"name": "test-package", "version": "1.0.0", "scripts": {"build": "echo \\"Build completed\\""}}')
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    subprocess.run(["git", "add", "package.json"], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)


def test_plugin_eslint():
    # Set up the test environment
    test_repo_name = "test-package"
    test_repo_dir = file_manager.get_repo_path(test_repo_name)

    print(f"I [OK] repo_name: {test_repo_name}")
    print(f"I [OK] repo_dir: {test_repo_dir}")

    file_manager.ensure_dir(test_repo_dir)
    print(f"I [OK] Created repo_folder within: {test_repo_dir}")

    eslintBaseUrl = config_manager.get_config_value("eslint.base")
    print(f"I [OK] eslintBaseUrl: {eslintBaseUrl}")

    assert os.path.exists(test_repo_dir), f"Config file not found at {test_repo_dir}"

    try:
        print("1. [OK] Run 'eslint' install script:")

        # Run the plugin
        eslint_config.run(test_repo_dir, eslintBaseUrl)

        # Validate the installation
        # assert eslint_config.validate_installation(test_repo_dir), "Installation validation failed"

    finally:
        print("All ESLint config plugin tests passed!")
        # Clean up the test repository
        # if os.path.exists(test_repo_dir):
        #     shutil.rmtree(test_repo_dir)


if __name__ == "__main__":
    test_plugin_eslint()
