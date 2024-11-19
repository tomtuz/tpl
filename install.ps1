# Installation based on 'pipx'

# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed. Please install Python 3.7 or later from https://www.python.org/downloads/"
    Write-Host "After installing Python, run this script again."
    exit 1
}

# Check if Poetry is installed
if (!(Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Poetry is not installed. Installing Poetry..."
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
}

# Run the build script
Write-Host "Building the tpl executable..."
python "scripts\build.py"

# Install the .whl file
pipx install --force "dist\tpl-0.1.0-py3-none-any.whl"

Write-Host "Installation complete. Please restart your terminal for changes to take effect."
Write-Host "You can now use the 'tpl' command to run the CLI tool."
tpl
Write-Host "You may need to restart your terminal for the changes to take effect."
