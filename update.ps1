# ~/username/.config/tpl
$tplDir = "$env:USERPROFILE\.config\tpl"

# ~/username/.config/templates
$tplTemplates = "$tplDir\templates"

# ~/username/.config/tpl
$tplBin = "$tplDir"

# Run the build script
Write-Host "Building the tpl executable..."
python "scripts\build.py"

# Copy the executable and templates to the installation directory
Copy-Item "dist\tpl.exe" -Destination "$tplBin\tpl.exe"
Copy-Item "dist\templates" -Destination "$tplTemplates\templates" -Recurse -Force

Write-Host "Installation complete. Please restart your terminal for changes to take effect."
Write-Host "You can now use the 'tpl' command to run the CLI tool."

# Initialize configuration
Write-Host "Initializing configuration..."
& "$tplBin\tpl.exe" config set initialized true

Write-Host "Configuration initialized. You can manage configuration using 'tpl config' commands."
