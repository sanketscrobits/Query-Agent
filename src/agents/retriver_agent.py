from src.schemas.response_schema import ResponseSchema
from src.utils.vector_db.index_strategies.pinecone_vector_index import PineconeVectorIndex

query_agent = PineconeVectorIndex.semantic_search()

def retriver_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    instruction = state["instruction"]
    modified_input = {"input": f"{user_query}\n\n{instruction}" if instruction else user_query}
    result = query_agent.invoke({"input": modified_input})
    response_str = result["output"]

    return {
        "user_query": user_query,
        "query_response": response_str,
        "evaluation_state": "",
        "retry_count": state["retry_count"] + 1,
        "instruction": instruction
    }
