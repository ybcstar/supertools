import pathlib, importlib.util, inspect, logging
from plugin_system.container import SecureLoader
from plugin_system.plugin import Plugin

logging.basicConfig(level=logging.INFO)

def scan(root_dir: pathlib.Path):
    plugins = {}
    for py in root_dir.rglob("*.py"):
        if py.name.startswith("_"):
            continue
        try:
            mod = SecureLoader.load(py)
            for _, cls in inspect.getmembers(mod, inspect.isclass):
                if issubclass(cls, Plugin) and cls is not Plugin:
                    key = f"{py.parent.name}.{cls.__name__}"
                    plugins[key] = cls
        except Exception as e:
            logging.error("Failed to load %s: %s", py, e)
    return plugins