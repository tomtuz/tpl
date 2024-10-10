import importlib.util
import os
import sys

from src.core.file_manager import get_config_dir


class PluginLoader:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = os.path.join(get_config_dir(), "plugins")

        # Ensure the plugins directory exists
        os.makedirs(self.plugin_dir, exist_ok=True)

    def load_plugins(self):
        print("plugin_dir: ", self.plugin_dir)
        if not os.path.exists(self.plugin_dir):
            print(f"Plugin directory does not exist: {self.plugin_dir}")
            return

        dirArr = os.listdir(self.plugin_dir)
        print("listdir: ", dirArr)

        # for filename in os.listdir(self.plugin_dir):
        for filename in dirArr:
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                plugin_path = os.path.join(self.plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)
                if hasattr(module, "register_plugin"):
                    self.plugins[plugin_name] = module.register_plugin()
                else:
                    print(f"Warning: Plugin '{plugin_name}' " "does not have a register_plugin function.")

    def get_plugin(self, plugin_name):
        return self.plugins.get(plugin_name)

    def list_plugins(self):
        return list(self.plugins.keys())


plugin_loader = PluginLoader()


def load_plugins():
    plugin_loader.load_plugins()


def get_plugin(plugin_name):
    return plugin_loader.get_plugin(plugin_name)


def list_plugins():
    return plugin_loader.list_plugins()
