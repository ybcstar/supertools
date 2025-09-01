from abc import ABC, abstractmethod

class Plugin(ABC):
    def __init__(self, root):
        self.root = root

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def run(self, ctx):
        pass

    def on_destroy(self):
        pass