# TPL - Template and Script Runner CLI

A personal CLI tool for managing project templates, configurations, and plugins.

### Prerequisites
- Python 3.11+ required
- Poetry for dependency management
- Global Configuration stored in `~/.config/tpl/config.json`

### Commands Tracking
- [x] **repository:**  Use repository templates
```sh
# interactive
> tpl repository
```

- [~] **config:**      Manage configuration settings for the TPL tool.
- [~] **template:**    Manage and use templates for file generation.
- [~] **plugin:**      Manage and use plugins to extend TPL functionality.
- [~] **spawn:**       Spawn new files or projects from templates.

## Quick Start

```sh
# (Linux) Run install script
# This links local package to $PATH with 'pipx'
1. ./install.sh OR ./install.ps1

# I.e.: 'tpl repository'
2. tpl <command> <options>
```

## Troubleshooting environment

- [DEBUG.md](./docs/DEBUG.md)

## Key Files

- `src/main.py`: Entry point
- `src/cli_selector/file.py`: Interactive CLI selector
- `src/core/commands.py`: Command implementations

**Managers**:
- `src/core/`
  - `config_manager.py`: Configuration management
  - `plugin_manager.py`: Plugin management
  - `git_manager.py`: Git management
  - `file_manager.py`: File management
  - `spawn_manager.py`: Spawn management

**Tests**:
- `tests/test_cli_commands.py`: CLI tests


## Dependency management

```sh
# Show outdated packages
poetry show --outdated

# Update packages
poetry update
poetry update <package1> <package2>

# Add/remove packages
poetry add/remove package_name
```

Always run tests after updating dependencies to ensure compatibility.
