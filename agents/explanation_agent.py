from prompts.legal_prompt import build_legal_prompt
from services.llm_service import generate_response


def explain_legal_text(user_query: str, language: str):

    prompt = build_legal_prompt(user_query=user_query, output_language=language)

    return generate_response(prompt)
