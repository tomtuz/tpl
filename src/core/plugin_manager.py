import importlib.util
import logging
import os
import shutil

from src.core.utils import get_script_dir

logger = logging.getLogger(__name__)


def get_plugins_dir() -> str:
    script_dir = get_script_dir()
    return os.path.normpath(os.path.join(script_dir, "plugins"))


def list_plugins() -> list[str]:
    plugins_dir = get_plugins_dir()
    return [f for f in os.listdir(plugins_dir) if f.endswith(".py") and f != "__init__.py"]


def install_plugin(plugin_path: str) -> None:
    plugins_dir = get_plugins_dir()
    plugin_name = os.path.basename(plugin_path)
    destination = os.path.normpath(os.path.join(plugins_dir, plugin_name))

    if os.path.exists(destination):
        raise ValueError(f"Plugin '{plugin_name}' already exists.")

    shutil.copy2(plugin_path, destination)
    logger.info(f"Plugin '{plugin_name}' installed successfully.")


def update_plugin(plugin_name: str, new_plugin_path: str) -> None:
    plugins_dir = get_plugins_dir()
    destination = os.path.normpath(os.path.join(plugins_dir, plugin_name))

    if not os.path.exists(destination):
        raise ValueError(f"Plugin '{plugin_name}' does not exist.")

    shutil.copy2(new_plugin_path, destination)
    logger.info(f"Plugin '{plugin_name}' updated successfully.")


def remove_plugin(plugin_name: str) -> None:
    plugins_dir = get_plugins_dir()
    plugin_path = os.path.normpath(os.path.join(plugins_dir, plugin_name))

    if not os.path.exists(plugin_path):
        raise ValueError(f"Plugin '{plugin_name}' does not exist.")

    os.remove(plugin_path)
    logger.info(f"Plugin '{plugin_name}' removed successfully.")


def get_plugin(plugin_name: str) -> object | None:
    plugins_dir = get_plugins_dir()
    plugin_path = os.path.normpath(os.path.join(plugins_dir, f"{plugin_name}.py"))

    if not os.path.exists(plugin_path):
        return None

    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def validate_plugin(plugin_path: str) -> bool:
    try:
        spec = importlib.util.spec_from_file_location("plugin", plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "run"):
            raise ValueError("Plugin must have a 'run' function.")

        return True
    except Exception as e:
        logger.error(f"Plugin validation failed: {str(e)}")
        return False
