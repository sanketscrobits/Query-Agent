from langchain.tools import tool
from src.utils.vector_db.vector_store_singleton import VectorStoreSingleton
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.vector_db.loader_strategies.local_loader import LocalLoader
from src.utils.vector_db.index_strategies.pinecone_vector_index import PineconeVectorIndex
from langchain_experimental.text_splitter import SemanticChunker


@tool
def get_context(query_text: str) -> str:
    """
    This function helps to answer user question by retrieving relevant context from documents.
    
    Args: 
        query_text: User question in string format
        
    Returns: 
        Context related to user's question in string format
    """

    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    document_loader_strategy = LocalLoader()
    vector_index_strategy = PineconeVectorIndex(embeddings=embeddings_model)
    # Build a semantic chunker callable compatible with our index API
    text_splitter = SemanticChunker(embeddings_model, breakpoint_threshold_type="percentile")
    def semantic_chunker(markdown_text: str):
        return text_splitter.create_documents([markdown_text])

    vector_store = VectorStoreSingleton(
        embeddings_model=embeddings_model,
        document_loader_strategy=document_loader_strategy,
        vector_index_strategy=vector_index_strategy,
        chunker=semantic_chunker,
    )

    result = vector_store.query(query_text = query_text)
    return result

if __name__ == "__main__":
    print(get_context("What initiative did the federal government announce regarding AI?"))