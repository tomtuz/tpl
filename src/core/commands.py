#!/usr/bin/env python3

import importlib.util
import logging
import os

from src.cli_selector.file import cli_selector_spawn
from src.core.config_manager import get_config_value, list_config_options, remove_config_value, set_config_value
from src.core.plugin_manager import (
    get_plugin,
    install_plugin,
    list_plugins,
    remove_plugin,
    update_plugin,
    validate_plugin,
)
from src.core.spawn_manager import list_templates, spawn_file, spawn_project
from src.utils.command_utils import handle_command_errors, log_command_args, validate_args
from src.utils.helpers import get_script_dir

SCRIPT_DIR = get_script_dir()
logger = logging.getLogger(__name__)


class CommandError(Exception):
    """Base exception for command-related errors."""
    pass


class ConfigError(CommandError):
    """Exception for configuration-related errors."""
    pass


class SpawnError(CommandError):
    """Exception for spawn-related errors."""
    pass


class TemplateError(CommandError):
    """Exception for template-related errors."""
    pass


class PluginError(CommandError):
    """Exception for plugin-related errors."""
    pass

# > tpl config get someKey
# > tpl config remove someKey
# > tpl config set someKey someValue
@validate_args(1, ConfigError, "Insufficient arguments for config command")
@handle_command_errors(ConfigError)
def cmd_config(args: list[str]) -> None:
    """
    Handle the 'config' command for getting, setting, removing configuration values, or listing all options.

    Args:
        args (List[str]): The arguments passed to the config command.
            [0]: action (get, set, remove, or list)
            [1]: key name (for get, set, remove)
            [2]: key value (only for 'set' action)
    """
    action = args[0]
    log_command_args("config", ["action", "key_name", "key_value"], args)

    if action == "list":
        options = list_config_options()
        print("Available config options:")
        for option in options:
            print(f"  {option}")
    elif action == "get":
        if len(args) < 2:
            raise ConfigError("Key name is required for 'get' action")
        key_name = args[1]
        config_value = get_config_value(key_name)
        print(f"[{key_name}]: {config_value}")
    elif action == "set":
        if len(args) < 3:
            raise ConfigError("Key name and value are required for 'set' action")
        key_name, key_value = args[1], args[2]
        set_config_value(key_name, key_value)
        print(f"Config value '{key_name}' has been set.")
    elif action == "remove":
        if len(args) < 2:
            raise ConfigError("Key name is required for 'remove' action")
        key_name = args[1]
        remove_config_value(key_name)
        print(f"Config value '{key_name}' has been removed.")
    else:
        raise ConfigError(f"Unknown config action: {action}")


# > tpl spawn
# > tpl spawn biome
# > tpl spawn biome base
@handle_command_errors(SpawnError)
def cmd_spawn(args: list[str]) -> None:
    """
    Handle the 'spawn' command for creating new files or projects from templates.

    If no arguments are provided, it runs the interactive CLI selector.
    Otherwise, it processes the provided template, filename/project name, and variant.

    Args:
        args (List[str]): The arguments passed to the spawn command.
            [0]: template_name
            [1]: filename or project_name
            [2]: variant (optional, for file spawning only)
    """
    logger.info("cmd_spawn called with args: %s", args)
    if not args:
        logger.info("Running spawn_cli.run_spawn()")
        cli_selector_spawn()
    elif args[0] == "list":
        templates = list_templates()
        print("Available templates:")
        for template in templates:
            print(f"  {template}")
    else:
        if len(args) < 2:
            raise SpawnError("Insufficient arguments. Usage: spawn <template_name> <filename/project_name> [variant]")

        template_name = args[0]
        name = args[1]
        variant = args[2] if len(args) > 2 else None

        log_command_args("spawn", ["template_name", "name", "variant"], args)

        if os.path.isdir(os.path.join(SCRIPT_DIR, "templates", template_name)):
            spawn_project(template_name, name)
            print(f"Project '{name}' spawned successfully from template '{template_name}'.")
        else:
            spawn_file(template_name, name, variant)
            print(f"File '{name}' spawned successfully from template '{template_name}'.")


# > tpl config template
# > tpl config template eslint
# > tpl config template eslint variation
@validate_args(2, TemplateError, "Insufficient arguments for template command")
@handle_command_errors(TemplateError)
def cmd_template(args: list[str]) -> None:
    """
    Handle the 'template' command for managing and using templates.

    Args:
        args (List[str]): The arguments passed to the template command.
            [0]: template_name
            [1]: command
            [2:]: options (optional)
    """
    template_name = args[0]
    command = args[1]
    options = args[2:] if len(args) > 2 else []

    log_command_args("template", ["template_name", "command", "options"], args)

    template_dir = os.path.join(SCRIPT_DIR, "templates", template_name)
    command_script = os.path.join(template_dir, f"{command}.py")

    if not os.path.exists(template_dir):
        raise TemplateError(f"Template '{template_name}' not found.")

    if not os.path.exists(command_script):
        raise TemplateError(f"Command '{command}' not found for template '{template_name}'.")

    spec = importlib.util.spec_from_file_location(f"{template_name}_{command}", command_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "run"):
        module.run(options)
    else:
        raise TemplateError(f"The '{command}' command for '{template_name}' template is not properly implemented.")


@validate_args(1, PluginError, "Insufficient arguments. Usage: plugin <action> [args]")
@handle_command_errors(PluginError)
def cmd_plugin(args: list[str]) -> None:
    """
    Handle the 'plugin' command for managing and using plugins.

    Args:
        args (List[str]): The arguments passed to the plugin command.
            [0]: action (list, install, update, remove, run)
            [1]: plugin_name (for install, update, remove, run actions)
            [2]: plugin_path (for install and update actions)
            [3:]: options (for run action)
    """
    action = args[0]
    log_command_args("plugin", ["action", "plugin_name", "plugin_path/options"], args)

    if action == "list":
        plugins = list_plugins()
        print("Available plugins:")
        for plugin in plugins:
            print(f"  {plugin}")
    elif action == "install":
        if len(args) < 3:
            raise PluginError("Plugin name and path are required for installation.")
        plugin_name, plugin_path = args[1], args[2]
        if validate_plugin(plugin_path):
            install_plugin(plugin_path)
            print(f"Plugin '{plugin_name}' installed successfully.")
        else:
            raise PluginError(f"Invalid plugin: {plugin_name}")
    elif action == "update":
        if len(args) < 3:
            raise PluginError("Plugin name and new path are required for update.")
        plugin_name, new_plugin_path = args[1], args[2]
        if validate_plugin(new_plugin_path):
            update_plugin(plugin_name, new_plugin_path)
            print(f"Plugin '{plugin_name}' updated successfully.")
        else:
            raise PluginError(f"Invalid plugin update: {plugin_name}")
    elif action == "remove":
        if len(args) < 2:
            raise PluginError("Plugin name is required for removal.")
        plugin_name = args[1]
        remove_plugin(plugin_name)
        print(f"Plugin '{plugin_name}' removed successfully.")
    elif action == "run":
        if len(args) < 2:
            raise PluginError("Plugin name is required to run a plugin.")
        plugin_name = args[1]
        options = args[2:]
        plugin = get_plugin(plugin_name)
        if plugin:
            plugin.run(options)
        else:
            raise PluginError(f"Unknown plugin: {plugin_name}")
    else:
        raise PluginError(f"Unknown plugin action: {action}")
