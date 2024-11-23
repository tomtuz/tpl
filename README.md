# TPL - Template and Script Runner CLI

A personal CLI tool for managing project templates, configurations, and plugins.

### Prerequisites
- Python 3.11+ required
- Poetry for dependency management
- Global Configuration stored in `~/.config/tpl/config.json`

## Quick Start

```sh

# (Linux) Run install script
# This links local package to $PATH with 'pipx'
./install.sh

# then just build and run
poetry build && tpl
# OR build and run in external path
poetry build
tpl

```

## Debug installation
```bash

# (Optional - 'pyenv')
# 1. Install python version from .python-version
poetry config virtualenvs.path ".venv"
poetry config virtualenvs.prefer-active-python true
pyenv install

# 2. verify Python version
pyenv local # verify python version
python3 --version # verify python version

# 3. Set Python to Poetry and create workspace
poetry env use 3.11.7
poetry install

# 4. Ensure Python version is correct
poetry env info
poetry env info --path
poetry env list
poetry env remove --all

# 5. Select Interpreter in VSCode
# -----

During poetry install the env will be created.
# Quickstart
poetry shell # (Ensure interpreter is active. Should be automatic, but check .python-version)
poetry install
poetry run build # 'poetry build' works too, but without scripts/build.py handler
pip install dist/tpl_cli-<version>-py3-none-any.whl
tpl --help

# Main commands
tpl spawn                                  # Interactive project spawning
tpl config [get|set|remove] [key] [value]  # Manage configurations
tpl template [template_name] [command]     # Use templates
tpl plugin [action] [plugin_name]          # Manage plugins

# Development commands
poetry run pytest                          # Run tests
poetry run build                           # Build the package
poetry run update                          # Update packages

# (dev.cmd) CLI heleper commands
install = "dev.cmd:install"
test = "dev.cmd:test"
refresh = "dev.cmd:refresh"
typecheck = "dev.cmd:typecheck"
lint = "dev.cmd:lint"
lintF = "dev.cmd:lintF"
format = "dev.cmd:format"
```

### Installing from PyPI

```bash
pip install tpl-cli

git clone https://github.com/your-repo/tpl.git
cd tpl

poetry install
poetry build
```

## Key Files

- `src/main.py`: Main entry point
- `src/cli_selector/file.py`: Interactive CLI selector
- `src/core/commands.py`: Command implementations
- `src/core/config_manager.py`: Configuration management
- `src/core/plugin_manager.py`: Plugin management
- `tests/test_cli_commands.py`: CLI tests


# Testing Externally
```sh
# setup and test in virtual env:
python -m venv venv && venv/Scripts/activate
cp C:\project-root\dist\tpl-0.1.0-py3-none-any.whl ./
pip install --force-reinstall .\tpl-0.1.0-py3-none-any.whl
tpl --help
```

## Dependency management

### Auto
1. Run update script. Review the output.
```sh
poetry run python scripts/update_dependencies.py
```
2. The script will:
    - Check for outdated packages
    - Update each package individually
    - Run tests after each update
    - Revert the update if tests fail
3. After the script completes, review the changes in `pyproject.toml` and `poetry.lock`.
4. If everything looks good, commit the changes:
    - `git add pyproject.toml poetry.lock`
    - `git commit -m "Update dependencies`

### Manual
```sh
# Show outdated packages
poetry show --outdated
# Update all packages
poetry update
# Update specific packages
poetry update package1 package2
# Add a new package
poetry add package_name
# Remove a package
poetry remove package_name
```

Always run tests after updating dependencies to ensure compatibility.
