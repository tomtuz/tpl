# Install pipx if not present
if (!(Get-Command pipx -ErrorAction SilentlyContinue)) {
    Write-Host "Installing pipx..."
    scoop install pipx
    pipx ensurepath
}

# Install cookiecutter using pipx
pipx install cookiecutter

# Add script directory to PATH
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$scriptPath*") {
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$scriptPath", "User")
}

Write-Host "Installation complete. Please restart your terminal for changes to take effect."
