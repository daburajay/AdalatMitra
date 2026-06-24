"""
utils/constants.py
Application constants
"""

# File paths
CAPTCHA_IMAGE_PATH = "captcha_temp.png"
CAPTCHA_ENHANCED_PATH = "captcha_enhanced.png"

# Court Code Map
COURT_CODE_MAP = {
    "Supreme Court of India": "sci",
    "Delhi High Court": "delhi",
    "Bombay High Court": "bombay",
    "Madras High Court": "madras",
    "Calcutta High Court": "calcutta",
    "Allahabad High Court": "allahabad",
    "Patna High Court": "patna",
    "Karnataka High Court": "karnataka",
    "Gujarat High Court": "gujarat",
    "Rajasthan High Court": "rajasthan",
}

# Supported Courts (for UI dropdown)
SUPPORTED_COURTS = [
    "Supreme Court of India",
    "Delhi High Court",
    "Bombay High Court",
    "Madras High Court",
    "Calcutta High Court",
    "Allahabad High Court",
    "Patna High Court",
    "Karnataka High Court",
    "Gujarat High Court",
    "Rajasthan High Court",
]

# Status Filters
STATUS_FILTERS = ["All", "Pending", "Disposed"]

# Language Options
LANGUAGE_OPTIONS = {
    "english": "English",
    "hindi": "Hindi",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "marathi": "Marathi",
    "bengali": "Bengali",
    "kannada": "Kannada",
    "malayalam": "Malayalam",
    "gujarati": "Gujarati",
    "punjabi": "Punjabi",
}

# Search Methods
SEARCH_METHODS = [
    "Case Number",
    "Party Name",
    "CNR Number",
    "Advocate Name",
    "FIR Number",
    "Filing Number"
]