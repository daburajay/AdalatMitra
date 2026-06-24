"""
services/district_court_service.py - District Court Service with Auto Discovery
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from bharat_courts import DistrictCourtClient
from bharat_courts.districtcourts.parser import parse_complex_value
from services.captcha_solver import DirectOCRSolver  # Auto CAPTCHA solver
from utils.logger import get_logger

logger = get_logger("district_court_service")


class DistrictCourtService:
    """Service for District Courts with auto-discovery and auto-CAPTCHA."""
    
    # Common state-district mappings for auto-discovery
    STATE_DISTRICT_MAP = {
        "8": {"name": "Bihar", "districts": {"1": "Patna"}},
        "7": {"name": "Delhi", "districts": {"1": "Central Delhi"}},
        "27": {"name": "Maharashtra", "districts": {"1": "Mumbai"}},
        "34": {"name": "Tamil Nadu", "districts": {"1": "Chennai"}},
        "29": {"name": "Karnataka", "districts": {"1": "Bangalore"}},
    }
    
    def __init__(self):
        self._case_types = None
        self._complex_cache = {}  # Cache discovered complexes
    
    def _get_solver(self):
        """Get auto CAPTCHA solver - SAME as High Court!"""
        return DirectOCRSolver()
    
    async def _discover_complex(self, state_code: str, district_code: str) -> Optional[str]:
        """Auto-discover court complex for a district."""
        
        cache_key = f"{state_code}_{district_code}"
        if cache_key in self._complex_cache:
            return self._complex_cache[cache_key]
        
        try:
            solver = self._get_solver()
            async with DistrictCourtClient(captcha_solver=solver) as client:
                # Get complexes for this district
                complexes = await client.list_complexes(state_code, district_code)
                
                if complexes:
                    # Take the first complex
                    first_key = list(complexes.keys())[0]
                    self._complex_cache[cache_key] = first_key
                    logger.info(f"✅ Auto-discovered complex: {complexes[first_key]} ({first_key})")
                    return first_key
                else:
                    logger.warning(f"No complexes found for state {state_code}, district {district_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to discover complex: {e}")
            return None
    
    async def search_cases(
        self,
        party_name: str,
        state_code: str = "7",
        district_code: str = "1",
        year: str = "2024",
        status: str = "Pending"
    ) -> Dict[str, Any]:
        """
        Search cases in district court by party name.
        Auto-discovers court complex.
        
        Args:
            party_name: Name of the party
            state_code: State code (default: "7" for Delhi)
            district_code: District code (default: "1")
            year: Filing year
            status: Status filter (Pending, Disposed, All)
        
        Returns:
            Dictionary with success status and cases list
        """
        try:
            # Auto-discover complex
            complex_key = await self._discover_complex(state_code, district_code)
            
            if not complex_key:
                return {
                    "success": False, 
                    "error": f"Could not discover court complex for state {state_code}, district {district_code}",
                    "cases": []
                }
            
            # Parse complex key
            code, ests, needs_est = parse_complex_value(complex_key)
            est = ests[0] if needs_est and ests else ""
            
            logger.info(f"Searching district court: state={state_code}, district={district_code}")
            logger.info(f"Complex: {complex_key}, Code: {code}, Est: {est}")
            logger.info(f"Party: {party_name}, Year: {year}, Status: {status}")
            
            # Auto CAPTCHA solver
            solver = self._get_solver()
            
            async with DistrictCourtClient(captcha_solver=solver) as client:
                # Map status filter
                status_map = {
                    "Pending": "Pending",
                    "Disposed": "Disposed", 
                    "All": "All",
                    "Listed": "Pending",
                    "Dismissed": "Disposed",
                    "Institution": "Pending"
                }
                api_status = status_map.get(status, "Pending")
                
                cases = await client.case_status_by_party(
                    state_code=state_code,
                    dist_code=district_code,
                    court_complex_code=code,
                    est_code=est,
                    party_name=party_name,
                    year=year,
                    status_filter=api_status
                )
                
                if not cases:
                    return {"success": True, "cases": [], "total": 0}
                
                # Get state/district names
                state_name = self.STATE_DISTRICT_MAP.get(state_code, {}).get("name", state_code)
                district_name = self.STATE_DISTRICT_MAP.get(state_code, {}).get("districts", {}).get(district_code, district_code)
                
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
                        "court": f"District Court, {district_name}",
                        "state": state_name,
                        "district": district_name,
                    })
                
                return {"success": True, "cases": results, "total": len(results)}
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"District Court search failed: {error_msg}")
            return {"success": False, "error": error_msg, "cases": []}
    
    async def search_case_by_number(
        self,
        case_number: str,
        state_code: str = "7",
        district_code: str = "1",
        year: str = "2024"
    ) -> Dict[str, Any]:
        """Search case by case number in district court."""
        try:
            # Auto-discover complex
            complex_key = await self._discover_complex(state_code, district_code)
            
            if not complex_key:
                return {"success": False, "error": "Could not discover court complex"}
            
            code, ests, needs_est = parse_complex_value(complex_key)
            est = ests[0] if needs_est and ests else ""
            
            solver = self._get_solver()
            
            async with DistrictCourtClient(captcha_solver=solver) as client:
                # Search by case number
                cases = await client.case_status(
                    state_code=state_code,
                    dist_code=district_code,
                    court_complex_code=code,
                    est_code=est,
                    case_type="",  # Auto-detect
                    case_number=case_number,
                    year=year
                )
                
                if not cases:
                    return {"success": False, "error": f"Case {case_number}/{year} not found"}
                
                case = cases[0]
                return {
                    "success": True,
                    "case_number": case.case_number,
                    "case_type": case.case_type,
                    "cnr_number": case.cnr_number,
                    "petitioner": case.petitioner,
                    "respondent": case.respondent,
                    "status": getattr(case, "status", "Pending"),
                    "next_hearing": str(getattr(case, "next_hearing_date", "Not scheduled")),
                }
                
        except Exception as e:
            logger.error(f"District Court case search failed: {e}")
            return {"success": False, "error": str(e)}