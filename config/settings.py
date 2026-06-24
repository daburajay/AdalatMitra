"""
config/settings.py
Configuration management
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Application Settings
DEFAULT_COURT = os.getenv("DEFAULT_COURT", "delhi")
DEFAULT_YEAR = os.getenv("DEFAULT_YEAR", "2024")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API Configuration
MAX_RETRIES = 3
CAPTCHA_MAX_ATTEMPTS = 3
REQUEST_TIMEOUT = 30

# Languages
SUPPORTED_LANGUAGES = [
    "English", "Hindi", "Tamil", "Telugu",
    "Marathi", "Bengali", "Kannada", "Malayalam",
    "Gujarati", "Punjabi"
]

# Note: SUPPORTED_COURTS is now defined in utils.constants
# to avoid circular imports