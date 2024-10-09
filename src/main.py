#!/usr/bin/env python3

import sys

from typing import List

from src.core.commands import cmd_spawn
from src.core.commands import cmd_template
from src.core.plugin_loader import load_plugins


def main(command: str = "", args: List[str] = []):
    load_plugins()

    if command is None:
        return
    elif command == "spawn":
        cmd_spawn(args)
    elif command == "template":
        cmd_template(args)
    # elif command == 'plugin':
    #     cmd_plugin(args)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: spawn, template, plugin")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: tpl <command> [args]")
        print("Available commands: spawn, template, plugin")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2:])
