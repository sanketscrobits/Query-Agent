from langchain.tools import tool
from src.utils.vector_db.vector_store_singleton import VectorStoreSingleton
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.vector_db.loader_strategies.local_loader import LocalLoader
from src.utils.vector_db.index_strategies.pinecone_vector_index import PineconeVectorIndex


@tool
def get_context(query_text: str) -> str:
    """
    This function helps to answer user question by retrieving relevant context from documents.
    
    Args: 
        query_text: User question in string format
        
    Returns: 
        Context related to user's question in string format
    """

    embeddings_model = HuggingFaceEmbeddings( model_name="all-MiniLM-L6-v2" )

    document_loader_strategy = LocalLoader
    vector_index_strategy = PineconeVectorIndex(embeddings = embeddings_model).semantic_search

    vector_store = VectorStoreSingleton(embeddings_model = embeddings_model,
                         document_loader_strategy = document_loader_strategy,
                         vector_index_strategy = vector_index_strategy)

    result = vector_store.query(query_text = query_text)
    return result


    '''try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        query_embedding = model.encode(query_text, convert_to_numpy=True)
        index = pc.Index(PINECONE_INDEX_NAME)

        results = index.query(
            vector=query_embedding.tolist(),
            top_k=20,
            include_metadata=True,
            score_threshold=0.7
        )
        
        if results["matches"]:
            context = results["matches"][0]["metadata"]["chunk_text"]
            return context
        else:
            return "No relevant context found for the question."
            
    except Exception as e:
        return f"Error retrieving context: {str(e)}"'''

if __name__ == "__main__":
    print(get_context("What initiative did the federal government announce regarding AI?"))