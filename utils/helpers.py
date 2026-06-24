"""
utils/helpers.py
Small reusable pure functions used across agents/services.
"""

import re


def parse_case_number(raw: str) -> tuple[str, str]:
    """
    Splits 'NUMBER/YEAR' into (number, year).
    Falls back to current year pattern if no slash given.
    Examples:
        '355/2024' -> ('355', '2024')
        '355'      -> ('355', '2024')   # caller should override default year
    """
    raw = raw.strip()
    if "/" in raw:
        parts = raw.split("/")
        number = parts[0].strip()
        year = parts[-1].strip()
        return number, year
    return raw, "2024"


def is_valid_cnr(cnr: str) -> bool:
    """CNR format: 4 letters + 6 digits + 4 digit year = 16 chars total."""
    if not cnr:
        return False
    pattern = r"^[A-Z]{4}\d{6}\d{4}$"
    return bool(re.match(pattern, cnr.strip().upper()))


def truncate(text: str, max_len: int = 40) -> str:
    text = text or ""
    return text if len(text) <= max_len else text[: max_len - 3] + "..."
