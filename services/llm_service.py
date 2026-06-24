from google import genai
from groq import Groq

from config.settings import (
    GEMINI_API_KEY,
    GROQ_API_KEY
)

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)

groq_client = Groq(
    api_key=GROQ_API_KEY
)


def generate_response(prompt: str):

    try:

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "provider": "Gemini",
            "response": response.text
        }

    except Exception as gemini_error:

        print(
            f"Gemini failed. Switching to Groq: {gemini_error}"
        )

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "provider": "Groq",
            "response": response.choices[0].message.content
        }