# tpl - Template and Script Runner

A CLI tool for project templating, script running, and configuration management.

## Prerequisites

- Python 3.7 or later
- Poetry (will be installed automatically if not present)

## Installation

The installation script will:
- Install `Poetry` if not already installed
- Build the standalone executable
- Copy the executable and templates to the appropriate directory
- Add the installation directory to your PATH

After installation, you may need to restart your terminal or reload your shell configuration for the `tpl` command to be available.

## Usage

Once installed, you can use the `tpl` command from anywhere in your terminal:

  ```
  tpl config <set/get/remove> <key> <value/-/->
  tpl spawn <key> <variation/->
  tpl template <key> <variation/->
  tpl plugin <key> <variation/->
  ```

## Development

### Run
To set up the development environment:

1. Clone the repository
2. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
3. Install dependencies: `poetry install`
4. Activate the virtual environment: `poetry shell`

To build the standalone executable:

```sh
  poetry install
  build
  poetry run python .\tests\0_test_file_spawn.py

  poetry run tpl spawn central base
```

### CLI commands
CLI commands are defined in a module file:
- `/dev/cmd.py`

**Command Examples:**

```sh
# 0. 'index'
tpl       # 'poetry run src.cli:run'

# 1. 'base'
pop       # 'poetry run src.cli:run' (name agnostic alias)
install   # 'poetry install'
build     # 'poetry run build'
test      # 'poetry pytest'
refresh   # 'poetry lock && poetry install && poetry run build'
typecheck # 'mypy .'

# 2. 'lint', 'format'
lint      # 'ruff check'
lintF     # 'ruff check --fix'
format    # 'ruff check --select I --fix && ruff format'
```

### Dependency Updating
```sh
1. > poetry show --outdated
2. update pyproject.toml versions
3. > refresh
```
