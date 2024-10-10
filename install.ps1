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

# ~/username/.config/tpl
$tplDir = "$env:USERPROFILE\.config\tpl"

# ~/username/.config/templates
$tplTemplates = "$tplDir\templates"

# ~/username/.config/tpl
$tplBin = "$tplDir"

Write-Host "tplDir: $tplDir"
Write-Host "tplTemplates: $tplTemplates"
Write-Host "tplBin: $tplBin"

# Create directory for tpl
New-Item -ItemType Directory -Force -Path $tplDir | Out-Null

# Run the build script
Write-Host "Building the tpl executable..."
python "scripts\build.py"

# Copy the executable and templates to the installation directory
Copy-Item "dist\tpl.exe" -Destination "$tplBin\tpl.exe"
Copy-Item "dist\templates" -Destination "$tplTemplates\templates" -Recurse -Force

# Add tpl directory to PATH
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$tplDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$tplDir", "User")
}

Write-Host "Installation complete. Please restart your terminal for changes to take effect."
Write-Host "You can now use the 'tpl' command to run the CLI tool."

# Initialize configuration
Write-Host "Initializing configuration..."
& "$tplBin\tpl.exe" config set initialized true

Write-Host "Configuration initialized. You can manage configuration using 'tpl config' commands."
