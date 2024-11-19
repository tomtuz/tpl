#!/bin/bash

set -e

echo "Runnning install.sh..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    echo "Examples:"
    echo "- [default]: sudo apt-get install python3"
    echo "- [pyenv]: pyenv install"
    echo "After installing Python, run this script again."
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

TPL_DIR="$HOME/.config/tpl"
TPL_TEMPLATES="$TPL_DIR/templates"
TPL_BIN="$TPL_DIR"

SRC_TEMPLATES="src/templates"

# Create directory for tpl
mkdir -p "$TPL_DIR"
mkdir -p "$TPL_TEMPLATES"

# Run the build script
echo "Building the tpl executable..."
python3 ./scripts/build.py

# Install the .whl file
pipx install --force "$TPL_BIN"/tpl-0.1.0-py3-none-any.whl

echo "Installation complete. You can now use the 'tpl' command."
echo "You may need to restart your terminal or run 'source ~/.bashrc' for the changes to take effect."


# # Initialize configuration
# echo "Initializing configuration..."
# pyenv global -m pip install "$TPL_BIN"/tpl-0.1.0-py3-none-any.whl
# pyenv exec pip install -r requirements.txt

# pyenv shell global
# python3 -m pip install "$TPL_BIN"/tpl-0.1.0-py3-none-any.whl
# # python3 -m pip install "$TPL_BIN"/tpl-0.1.0-py3-none-any.whl config set initialized true

# # "$TPL_BIN"/tpl config set initialized true
# # "$TPL_BIN"/tpl config set initialized true

echo "Configuration initialized. You can manage configuration using 'tpl config' commands."


# # Add ~/.config/tpl to PATH if it's not already there
# if [[ ":$PATH:" != *":$TPL_DIR:"* ]]; then
#     echo "Updated PATH with tpl: {$TPL_DIR}"
#     echo 'export PATH=$PATH:$TPL_DIR' >> ~/.bashrc
#     export PATH=$PATH:$TPL_DIR
# fi

