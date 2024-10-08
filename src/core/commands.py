#!/usr/bin/env python3

import sys
import os
import importlib.util
from src.core.config_manager import get_config_value, set_config_value, remove_config_value
from src.core.utils import get_script_dir, get_file_index_path, getFile, print_all_indexes
from src.core.plugin_loader import get_plugin, list_plugins


SCRIPT_DIR = get_script_dir()

# > tpl config get someKey
# > tpl config remove someKey
# > tpl config set someKey someValue
def cmd_config(args):
    # max 3 options

    if len(args) < 1:
        print("Usage: tpl config <action> [args]")
        print("Available actions: get, set, remove")
        sys.exit(1)

    action = args[0]
    keyName = args[1]
    keyValue = args[2]
    options = args[3]

    if action == "get":
        if len(args) != 2:
            print("Usage: tpl config get <key>")
            sys.exit(1)
        configValue = get_config_value(keyName)
        print(f"[{keyName}]: {configValue}")

    elif action == "set":
        if len(args) != 3:
            print("Usage: tpl config set <key> <value>")
            sys.exit(1)
        set_config_value(keyName, keyValue)
        print(f"Config value '{keyName}' has been set.")

    elif action == "remove":
        if len(args) != 2:
            print("Usage: tpl config remove <key>")
            sys.exit(1)
        remove_config_value(keyName)
        print(f"Config value '{keyName}' has been removed.")

    else:
        print(f"Unknown config action: {keyName}")
        print("Available actions: get, set, remove")
        sys.exit(1)

# > tpl spawn
# > tpl spawn biome
# > tpl spawn biome base
def cmd_spawn(args):
    if len(args) < 2:
        print("Usage: spawn <filename> <variant>")
        return

    filename = args[0]
    variant = args[1]
    print("SPAWN:")
    print(f"- filename: {filename}")
    print(f"- variant: {variant}")

    return getFile(filename, variant)

    if (filename):
      return getFile(filename)
    else:
      print("[FAIL] file index doesn't exist.")
      file_index_path = get_file_index_path()
      print_all_indexes(file_index_path)
      return 1

# > tpl config template
# > tpl config template eslint
# > tpl config template eslint variation
def cmd_template(template_name, command, args):
    if len(args) < 2:
        print("Usage: template <template_name> <command> [options]")
        return

    template_name = args[0]
    command = args[1]
    options = args[2:]

    # Implement template logic here
    print(f"Running template: {template_name}")
    print(f"Command: {command}")
    print(f"Options: {options}")

    script_dir = get_script_dir()
    template_dir = os.path.join(script_dir, "templates", template_name)
    
    if not os.path.exists(template_dir):
        print(f"Template '{template_name}' not found.")
        sys.exit(1)
    
    command_script = os.path.join(template_dir, f"{command}.py")
    
    if not os.path.exists(command_script):
        print(f"Command '{command}' not found for template '{template_name}'.")
        sys.exit(1)
    
    spec = importlib.util.spec_from_file_location(f"{template_name}_{command}", command_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if hasattr(module, 'run'):
        module.run(args)
    else:
        print(f"The '{command}' command for '{template_name}' template is not properly implemented.")
        sys.exit(1)


def cmd_plugin(args):
    if len(args) < 1:
        print("Usage: plugin <plugin_name> [options]")
        print("Available plugins:")
        for plugin in list_plugins():
            print(f"  {plugin}")
        return

    plugin_name = args[0]
    options = args[1:]

    plugin = get_plugin(plugin_name)
    if plugin:
        plugin.run(options)
    else:
        print(f"Unknown plugin: {plugin_name}")
