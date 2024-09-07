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

# Install Poetry if not present
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    pipx install poetry
    # curl -sSL https://install.python-poetry.org | python3 -
fi

# Add Poetry to PATH if it's not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
    export PATH=$PATH:$HOME/.local/bin
fi

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create ~/.local/bin if it doesn't exist
mkdir -p ~/.local/bin

# Copy the tpl script and tpl_core.py to ~/.local/bin
cp "$SCRIPT_DIR/tpl" ~/.local/bin/tpl
cp "$SCRIPT_DIR/tpl_core.py" ~/.local/bin/tpl_core.py

# Make sure the tpl script is executable
chmod +x ~/.local/bin/tpl

echo "Installation complete. You can now use the 'tpl' command. You may need to restart your terminal or run 'source ~/.bashrc' for the changes to take effect."
