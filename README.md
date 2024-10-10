# TPL - Template and Script Runner CLI

A personal CLI tool for managing project templates, configurations, and plugins.

### Prerequisites
- Python 3.11+ required
- Poetry for dependency management
- Global Configuration stored in `~/.config/tpl/config.json`

## Quick Start

```bash
# Quickstart
poetry install
poetry build
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
