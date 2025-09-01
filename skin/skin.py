from abc import ABC, abstractmethod

class Skin(ABC):
    @abstractmethod
    def apply(self, root, skin_data):
        pass