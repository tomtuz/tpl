
```markdown
# tpl - Template and Script Runner

A simple tool to create Poetry projects and run custom scripts.

## Installation

### Linux/macOS
Run `./install.sh`

### Windows
Run `install.ps1` in PowerShell

## Usage

1. Create a new Poetry project:
   ```
   tpl poetry <project_name>
   ```

2. Run a script from the script template:
   ```
   tpl script <script_name>
   ```

## Adding Custom Scripts

Place your custom scripts in the `templates/script/` directory. Supported file types:
- Python (.py)
- Bash (.sh)

Example:
- `templates/script/index.sh`
- `templates/script/custom_script.py`

