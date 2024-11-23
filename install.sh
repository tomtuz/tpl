#!/bin/bash

# Installation based on 'pipx'

set -e
echo "Runnning [install.sh]..."

# [CHECK] if 'Python' is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    echo "Examples:"
    echo "- [default]: sudo apt-get install python3"
    echo "- [pyenv]: pyenv install <version> (pyenv install --list)"
    echo "After installing Python, run this script again."
    exit 1
fi

# [CHECK] if 'git' is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git git not installed."
    echo "After [git], run this script again."
    exit 1
fi

# [CHECK] if 'Poetry' is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# [RUN] the build script
echo "Building [tpl] package..."
python3 ./scripts/build.py

# [INSTALL] the .whl file
WHEEL_FILE=$(ls ./dist/tpl-*.whl | head -n 1)
if [ -z "$WHEEL_FILE" ]; then
    echo "Error: No .whl file found in the dist directory."
    exit 1
fi
pipx install --force "$WHEEL_FILE"

# [CHECK] if 'tpl' is installed
if command -v tpl &> /dev/null; then
  echo "Installation complete. You can now use the 'tpl' command."
else
  echo "Installation error"
  exit 1
fi

# [STATUS] display package status
tpl
echo "You may need to restart your terminal or run 'source ~/.bashrc' for the changes to take effect."
