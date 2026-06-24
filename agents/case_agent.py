# agents/case_agent.py

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from services.bharat_court_service import (
    fetch_cases_by_party,
    fetch_case_by_number,
    fetch_case_types,
    fetch_orders,
)


@dataclass
class CaseResult:
    """Standardized case result from the agent layer."""
    success: bool
    case_number: str = ""
    case_type: str = ""
    cnr_number: str = ""
    filing_number: str = ""
    court_name: str = ""
    petitioner: str = ""
    respondent: str = ""
    status: str = ""
    next_hearing: str = ""
    error: str = ""
    total_cases: int = 0
    cases: List[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "case_number": self.case_number,
            "case_type": self.case_type,
            "cnr_number": self.cnr_number,
            "filing_number": self.filing_number,
            "court_name": self.court_name,
            "petitioner": self.petitioner,
            "respondent": self.respondent,
            "status": self.status,
            "next_hearing": self.next_hearing,
            "error": self.error,
            "total_cases": self.total_cases,
            "cases": self.cases or [],
        }


def search_by_party(
    party_name: str,
    court_name: str = "Delhi High Court",
    year: str = "2024",
    status_filter: str = "Pending",
    captcha_answer: str = "",
) -> Dict[str, Any]:
    """
    Search for cases by party name.
    
    Args:
        party_name: Name of the party to search for
        court_name: Name of the court
        year: Filing year
        status_filter: Case status filter
        captcha_answer: Optional CAPTCHA answer (if not provided, will be handled by service)
    
    Returns:
        Dict with success, cases, total, and error fields
    """
    return fetch_cases_by_party(
        court_name=court_name,
        party_name=party_name,
        year=year,
        status_filter=status_filter,
        captcha_answer=captcha_answer,
    )


def search_by_party_interactive(
    party_name: str,
    court_name: str = "Delhi High Court",
    year: str = "2024",
    status_filter: str = "Pending",
) -> Dict[str, Any]:
    """
    Search for cases by party name with interactive CAPTCHA prompting.
    This version will always prompt the user for CAPTCHA if needed.
    
    Args:
        party_name: Name of the party to search for
        court_name: Name of the court
        year: Filing year
        status_filter: Case status filter
    
    Returns:
        Dict with success, cases, total, and error fields
    """
    return fetch_cases_by_party(
        court_name=court_name,
        party_name=party_name,
        year=year,
        status_filter=status_filter,
        auto_prompt=True,  # This will prompt the user for CAPTCHA
    )


def track_case_with_known_type(
    case_number: str,
    court_name: str = "Delhi High Court",
    case_type: str = "",
    year: str = "2024",
    captcha_answer: str = "",
) -> CaseResult:
    """
    Track a specific case when you already know the case type.
    
    Args:
        case_number: Case number (e.g., "12345/2024")
        court_name: Name of the court
        case_type: Case type ID (from fetch_case_types)
        year: Filing year
        captcha_answer: Optional CAPTCHA answer
    
    Returns:
        CaseResult object
    """
    # Extract year from case number if not provided
    if "/" in case_number and not year:
        parts = case_number.split("/")
        case_number = parts[0]
        year = parts[1] if len(parts) > 1 else "2024"
    
    result = fetch_case_by_number(
        court_name=court_name,
        case_type=case_type,
        case_number=case_number,
        year=year,
        captcha_answer=captcha_answer,
    )
    
    if result.get("success"):
        return CaseResult(
            success=True,
            case_number=result.get("case_number", ""),
            case_type=result.get("case_type", ""),
            cnr_number=result.get("cnr_number", ""),
            filing_number=result.get("filing_number", ""),
            court_name=result.get("court_name", ""),
            petitioner=result.get("petitioner", ""),
            respondent=result.get("respondent", ""),
            status=result.get("status", ""),
            next_hearing=result.get("next_hearing", ""),
        )
    else:
        return CaseResult(
            success=False,
            error=result.get("error", "Unknown error"),
        )


def get_case_types(court_name: str = "Delhi High Court") -> Dict[str, str]:
    """
    Get all case types for a court.
    
    Args:
        court_name: Name of the court
    
    Returns:
        Dict mapping case type IDs to names
    """
    return fetch_case_types(court_name)


def get_case_orders(
    court_name: str,
    case_type: str,
    case_number: str,
    year: str,
) -> List[Dict]:
    """
    Get orders/hearings for a specific case.
    
    Args:
        court_name: Name of the court
        case_type: Case type ID
        case_number: Case number
        year: Filing year
    
    Returns:
        List of order dictionaries
    """
    return fetch_orders(court_name, case_type, case_number, year)