import pathlib, importlib.util, inspect

SAFE_MODULES = {"ttkbootstrap", "tkinter", "math", "time", "threading"}

class SecureLoader:
    @staticmethod
    def load(path):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

class Container:
    _services = {}
    @classmethod
    def register(cls, name, obj): cls._services[name] = obj
    @classmethod
    def get(cls, name, default=None): return cls._services.get(name, default)