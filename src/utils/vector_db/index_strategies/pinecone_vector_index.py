from src.utils.vector_db.index_strategies.base import VectorIndexStrategy
from settings import PINECONE_API_KEY, PINECONE_INDEX_NAME
from pinecone import Pinecone

class PineconeVectorIndex(VectorIndexStrategy):
    def  __init__ (self, embeddings):
        self.__collection_name = PINECONE_INDEX_NAME
        self.__api_key = Pinecone(api_key=PINECONE_API_KEY)
        self.__embeddings=embeddings
        self.__collection = None

    def create_or_load_vector_index(self, chunks):
        if not self.__collection:
            pinecone_vectors = []
            for i, (embedding, chunk) in enumerate(zip(self.__embeddings, chunks)):
                vector_data = {
                    "id": f"chunk_{i}",
                    "values": embedding.tolist(),
                    "metadata": {
                        "chunk_text": chunk.page_content,
                        "chunk_id": i,
                        "source": "documents_folder"
                    }
                }
                pinecone_vectors.append(vector_data)
            self.__name.upsert(vectors=pinecone_vectors)
        print(f"Uploaded {len(pinecone_vectors)} chunks to Pinecone index '{self.__collection}'")
        return self
    
    def semantic_search(self, embeded_query) -> str:
        collection = self.__api_key.Index(self.__collection_name)
        response = collection.query(
            vector=embeded_query.tolist(),
            top_k=20,
            include_metadata=True,
            score_threshold=0.7
        )
        if response["matches"]:
            context = response["matches"][0]["metadata"]["chunk_text"]
            return context
        else:
            return "No relevant context found for the question."


"""import sys
from pathlib import Path
from langchain_experimental.text_splitter import SemanticChunker
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from settings import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_REGION, GOOGLE_API_KEY
from src.document_loader.local_loader import get_combined_text
from src.utils.vector_db.index_strategies.base import vector_index_strategies
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools.query_tool import get_context
from src.utils.yaml_loader import load_prompts

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

class chunking_and_embedding:

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    semantic_chunker = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    def semantic_chunking(self, text: str):
        text_splitter = SemanticChunker(
            self.semantic_chunker,
            breakpoint_threshold_type="percentile"
        )
        chunks = text_splitter.create_documents([text])
        print(f"Created {len(chunks)} semantic chunks")
        return chunks
    
    def embed_chunks(self, chunks):
        chunk_texts = [chunk.page_content for chunk in chunks]
        embeddings = self.embedding_model.encode(chunk_texts, convert_to_numpy=True)
        print(f"Generated embeddings for {len(embeddings)} chunks")
        return embeddings
    
    def embedding(self, documents_dir: str = "documents"):
        combined_text = get_combined_text(documents_dir)
        
        if not combined_text or "No readable content found" in combined_text:
            print("No content to upload")
            return
        
        chunks = self.semantic_chunking(combined_text)
        embeddings = self.embed_chunks(chunks)
        return embeddings, chunks


class pinecone_vector_index(vector_index_strategies):
    def __init__(self, PINECONE_INDEX_NAME, PINECONE_API_KEY, path: str):
        self.pinecone_apikey = Pinecone(api_key=PINECONE_API_KEY)
        self.
        self.path = 
        self.collection = None

    def create_or_load_vectorstore(self):

    def query(self,text):
        llm = ChatGoogleGenerativeAI( model= "gemini-2.0-flash", temperature= 0.1, google_api_key=GOOGLE_API_KEY )
        tools = [get_context]
        prompts = load_prompts(prompt_path = "src/utils/prompts.yml")
        prompt_text = prompts["query_agent_prompt"]
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_text),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_functions_agent(llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
"""