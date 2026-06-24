"""
services/bharat_court_service.py - Bharat Court API Wrapper with Auto CAPTCHA
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from bharat_courts import get_court, HCServicesClient
from services.captcha_solver import DirectOCRSolver  # Auto CAPTCHA resolver
from utils.logger import get_logger
from utils.constants import COURT_CODE_MAP

logger = get_logger("bharat_court_service")


class BharatCourtService:
    """Service for Bharat Courts API with Auto CAPTCHA."""
    
    def __init__(self, court_name: str = "Delhi High Court"):
        self.court_name = court_name
        self.court_code = COURT_CODE_MAP.get(court_name, "delhi")
        self.court = get_court(self.court_code)
        self._case_types = None
    
    def _get_solver(self):
        """Get auto CAPTCHA solver (OCR) - No manual entry needed!"""
        return DirectOCRSolver()
    
    def fetch_case_types(self) -> Dict[str, str]:
        """Fetch case types."""
        try:
            async def _fetch():
                solver = self._get_solver()
                async with HCServicesClient(captcha_solver=solver) as client:
                    raw = await client.list_case_types(self.court)
                    if isinstance(raw, dict):
                        return raw
                    return {str(ct.id): ct.name for ct in raw}
            self._case_types = asyncio.run(_fetch())
            return self._case_types
        except Exception as e:
            logger.error(f"Failed to fetch case types: {e}")
            return {"83": "LA.APP.", "134": "W.P.(C)"}
    
    async def search_cases(
        self,
        party_name: str,
        year: str = "2024",
        status: str = "Pending"
    ) -> Dict[str, Any]:
        """
        Search cases by party name, year, and status.
        Auto CAPTCHA handled by DirectOCRSolver.
        """
        try:
            # Map status to API filter
            status_map = {
                "pending": "Pending",
                "listed": "Pending",
                "disposed": "Pending",
                "dismissed": "Pending",
                "institution": "Pending",
                "all": "Pending",
            }
            
            api_status = status_map.get(status.lower(), "Pending")
            
            # Auto CAPTCHA solver - no CLI prompt!
            solver = self._get_solver()
            
            async with HCServicesClient(captcha_solver=solver) as client:
                logger.info(f"Searching: {party_name}, {year}, {status}")
                cases = await client.case_status_by_party(
                    self.court,
                    party_name=party_name,
                    year=year,
                    status_filter=api_status
                )
                
                if not cases:
                    return {"success": True, "cases": [], "total": 0}
                
                # Convert cases to dict
                results = []
                for case in cases:
                    results.append({
                        "case_number": case.case_number,
                        "case_type": case.case_type,
                        "cnr_number": case.cnr_number,
                        "petitioner": case.petitioner,
                        "respondent": case.respondent,
                        "status": getattr(case, "status", status),
                        "next_hearing": str(getattr(case, "next_hearing_date", "Not scheduled")),
                        "filing_number": getattr(case, "filing_number", "N/A"),
                        "registration_date": str(getattr(case, "registration_date", "N/A")),
                        "court": self.court_name,
                    })
                
                return {"success": True, "cases": results, "total": len(results)}
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Search failed: {error_msg}")
            return {"success": False, "error": error_msg, "cases": []}