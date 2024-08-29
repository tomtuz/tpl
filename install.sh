#!/bin/bash

set -e

# Install pipx if not present
if ! command -v pipx &> /dev/null; then
    echo "Installing pipx..."
    sudo apt install pipx
    pipx ensurepath
fi

# Install cookiecutter using pipx
pipx install cookiecutter

# Add tpl.py to PATH
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "export PATH=\$PATH:$SCRIPT_DIR" >> ~/.bashrc
source ~/.bashrc

echo "Installation complete. Please restart your terminal or source your .bashrc file."
