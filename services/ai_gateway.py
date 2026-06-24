"""
services/ai_gateway.py
AI Gateway - Central entry point for all AI calls
Gemini Primary | Groq Fallback
"""

from typing import Optional, Dict, Any
from google import genai
from groq import Groq
from config.settings import GEMINI_API_KEY, GROQ_API_KEY
from utils.logger import get_logger

logger = get_logger("ai_gateway")

class AIGateway:
    """
    AI Gateway - Single entry point for AI operations.
    Primary: Gemini | Fallback: Groq
    """
    
    def __init__(self):
        self._gemini_client = None
        self._groq_client = None
        self._gemini_available = False
        self._groq_available = False
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize both AI services."""
        # Initialize Gemini
        try:
            if GEMINI_API_KEY:
                self._gemini_client = genai.Client(api_key=GEMINI_API_KEY)
                self._gemini_available = True
                logger.info("✅ Gemini initialized successfully")
            else:
                logger.warning("GEMINI_API_KEY not found")
        except Exception as e:
            logger.warning(f"Gemini initialization failed: {e}")
        
        # Initialize Groq (Fallback)
        try:
            if GROQ_API_KEY:
                self._groq_client = Groq(api_key=GROQ_API_KEY)
                self._groq_available = True
                logger.info("✅ Groq initialized successfully")
            else:
                logger.warning("GROQ_API_KEY not found")
        except Exception as e:
            logger.warning(f"Groq initialization failed: {e}")
        
        if not self._gemini_available and not self._groq_available:
            logger.error("❌ No AI services available")
    
    def generate_response(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Generate response using available AI services.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
        
        Returns:
            Dictionary with provider and response text
        """
        # Try Gemini first
        if self._gemini_available:
            try:
                logger.info("Using Gemini for generation")
                response = self._gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "max_output_tokens": max_tokens,
                        "temperature": 0.7
                    }
                )
                return {
                    "provider": "Gemini",
                    "response": response.text,
                    "success": True
                }
            except Exception as e:
                logger.warning(f"Gemini failed: {e}, falling back to Groq")
        
        # Fallback to Groq
        if self._groq_available:
            try:
                logger.info("Using Groq as fallback")
                response = self._groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return {
                    "provider": "Groq",
                    "response": response.choices[0].message.content,
                    "success": True
                }
            except Exception as e:
                logger.error(f"Groq failed: {e}")
        
        return {
            "provider": "None",
            "response": "No AI services available. Please check your API keys.",
            "success": False
        }
    
    def generate_stream(self, prompt: str, max_tokens: int = 500):
        """
        Generate streaming response.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
        
        Yields:
            Chunks of generated text
        """
        if self._gemini_available:
            try:
                response = self._gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "max_output_tokens": max_tokens,
                        "temperature": 0.7
                    },
                    stream=True
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
                return
            except Exception as e:
                logger.warning(f"Gemini streaming failed: {e}")
        
        # Fallback to Groq (non-streaming)
        if self._groq_available:
            try:
                response = self._groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                yield response.choices[0].message.content
            except Exception as e:
                logger.error(f"Groq failed: {e}")
                yield "Error: Failed to generate response"
        else:
            yield "No AI services available"