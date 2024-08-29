#!/usr/bin/env python3

import sys
import os
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: tpl <template_name>")
        sys.exit(1)

    template_name = sys.argv[1]
    script_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_dir, "templates", template_name)

    if not os.path.exists(template_path):
        print(f"Template '{template_name}' not found.")
        sys.exit(1)

    subprocess.run(["cookiecutter", template_path])

if __name__ == "__main__":
    main()
