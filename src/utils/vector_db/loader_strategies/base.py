from abc import ABC, abstractmethod

class DocumentLoaderStrategy(ABC):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def load_documents(self, path) -> list:
        pass
