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

To set up the development environment:

1. Clone the repository
2. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
3. Install dependencies: `poetry install`
4. Activate the virtual environment: `poetry shell`

To build the standalone executable:

```sh
  poetry install
  poetry run python build.py
  poetry run python .\tests\0_test_file_spawn.py

  poetry run tpl spawn central base
```
