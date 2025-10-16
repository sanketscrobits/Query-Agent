from abc import ABC, abstractmethod
from langchain_huggingface import HuggingFaceEmbeddings

class VectorIndexStrategy(ABC):

    @abstractmethod
    def create_or_load_vector_index(self, chunks):
        pass

    @abstractmethod
    def semantic_search(self, embeded_query:HuggingFaceEmbeddings) -> str:
        pass
