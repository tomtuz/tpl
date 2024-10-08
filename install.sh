#!/bin/bash

set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    echo "You can typically install Python 3 using your system's package manager."
    echo "For example, on Ubuntu or Debian: sudo apt-get install python3"
    echo "After installing Python, run this script again."
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

TPL_DIR="$HOME/.config/tpl"
TPL_TEMPLATES = "$TPL_DIR/templates"
TPL_BIN = "$TPL_DIR"

# Create directory for tpl
mkdir -p "$TPL_DIR"

# Run the build script
echo "Building the tpl executable..."
python3 ./scripts/build.py

# Copy the executable and templates to the installation directory
cp dist/tpl.exe "$TPL_DIR"
cp -r dist/templates "$TPL_TEMPLATES"

# Make sure the tpl executable is... executable
chmod +x "$TPL_DIR"

# Add ~/.config/tpl to PATH if it's not already there
if [[ ":$PATH:" != *":$TPL_DIR:"* ]]; then
    echo 'export PATH=$PATH:$TPL_DIR' >> ~/.bashrc
    export PATH=$PATH:$TPL_DIR
fi

echo "Installation complete. You can now use the 'tpl' command."
echo "You may need to restart your terminal or run 'source ~/.bashrc' for the changes to take effect."

# Initialize configuration
echo "Initializing configuration..."
"$TPL_DIR" config set initialized true

echo "Configuration initialized. You can manage configuration using 'tpl config' commands."
