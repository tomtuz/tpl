#!/bin/bash

# Installation based on 'pipx'

set -e
echo "Runnning [install.sh]..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    echo "Examples:"
    echo "- [default]: sudo apt-get install python3"
    echo "- [pyenv]: pyenv install <version> (pyenv install --list)"
    echo "After installing Python, run this script again."
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Run the build script
echo "Building [tpl] package..."
python3 ./scripts/build.py

# Install the .whl file
pipx install --force dist/tpl-0.1.0-py3-none-any.whl

echo "Installation complete. You can now use the 'tpl' command."
tpl
echo "You may need to restart your terminal or run 'source ~/.bashrc' for the changes to take effect."
