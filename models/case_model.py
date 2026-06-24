"""
models/case_model.py
Defines the shape of case data used across every agent.
Using dataclasses (not pydantic) to keep Phase 1 dependency-free.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaseModel:
    """Core case info — what case_agent.py returns after a successful lookup."""

    success: bool = False
    error: Optional[str] = None

    case_number: str = "N/A"
    case_type: str = "N/A"
    cnr_number: str = "N/A"
    filing_number: str = "N/A"

    court_name: str = "N/A"
    petitioner: str = "N/A"
    respondent: str = "N/A"

    status: str = "N/A"
    stage: str = "N/A"
    next_hearing: str = "N/A"

    type_id: Optional[str] = None  # internal court-specific case_type code

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "error": self.error,
            "case_number": self.case_number,
            "case_type": self.case_type,
            "cnr_number": self.cnr_number,
            "filing_number": self.filing_number,
            "court_name": self.court_name,
            "petitioner": self.petitioner,
            "respondent": self.respondent,
            "status": self.status,
            "stage": self.stage,
            "next_hearing": self.next_hearing,
        }

    @staticmethod
    def error_response(message: str) -> "CaseModel":
        return CaseModel(success=False, error=message)
