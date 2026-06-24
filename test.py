from services.llm_service import LLMService

result = LLMService.generate_response("Explain bail in simple Hindi.")

print(result["provider"])
print(result["response"])
