#!/usr/bin/env python3

import sys
import os
import subprocess

def create_poetry_project(project_name):
    subprocess.run(["poetry", "new", project_name])
    os.chdir(project_name)
    subprocess.run(["poetry", "install"])
    print(f"Poetry project '{project_name}' has been created and dependencies installed.")

def run_script(script_name):
    print("script_name: ", script_name)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(script_dir, "templates", script_name, "script")

    if not os.path.exists(script_path):
        print(f"Script '{script_name}' not found.")
        sys.exit(1)

    file_extension = os.path.splitext(script_name)[1].lower()
    
    if file_extension == '.py':
        subprocess.run(["python", script_path])
    elif file_extension == '.sh':
        subprocess.run(["bash", script_path])
    else:
        print(f"Unsupported script type: {script_name}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: tpl <command> [args]")
        print("Commands:")
        print("  poetry <project_name>  - Create a new Poetry project")
        print("  script <script_name>   - Run a script from the script template")
        sys.exit(1)

    command = sys.argv[1]

    if command == "poetry":
        if len(sys.argv) < 3:
            print("Usage: tpl poetry <project_name>")
            sys.exit(1)
        create_poetry_project(sys.argv[2])
    elif command == "script":
        if len(sys.argv) < 3:
            print("Usage: tpl script <script_name>")
            sys.exit(1)
        run_script(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
