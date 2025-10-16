from src.schemas.response_schema import ResponseSchema
from guardrails import Guard
from guardrails.hub import  ProfanityFree
from guardrails.errors import ValidationError


guard = Guard().use(
    ProfanityFree, on_fail="exception"
)

def evaluator_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    query_response = state["query_response"]
    llm_text = query_response
    if state["retry_count"] > 3:
        return {
            "user_query": user_query,
            "query_response": "Max retries exceeded. Response could not be generated without profanity.",
            "evaluation_state": "True",
            "instruction": "" 
        }

    try:
        validated_output = guard.validate(llm_text)
        return {
            "user_query": user_query,
            "query_response": str(validated_output), 
            "evaluation_state": "True",
            "instruction": ""
        }
    except ValidationError:
        retry_instruction = "Rephrase the response to be completely profanity-free. Avoid any explicit language, slurs, or direct quotes of offensive content. Summarize factually and neutrally."
        return {
            "user_query": user_query,
            "query_response": llm_text,  
            "evaluation_state": "False",
            "instruction": retry_instruction
        }