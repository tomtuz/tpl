import os
import importlib.util
import sys

class PluginLoader:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                plugin_path = os.path.join(self.plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)
                if hasattr(module, 'register_plugin'):
                    self.plugins[plugin_name] = module.register_plugin()
                else:
                    print(f"Warning: Plugin '{plugin_name}' does not have a register_plugin function.")

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
