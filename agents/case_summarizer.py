"""
agents/case_summarizer.py - AI Case Summarizer
"""

from typing import Dict, Any
from services.ai_gateway import AIGateway
from utils.logger import get_logger

logger = get_logger("case_summarizer")

class CaseSummarizer:
    """Summarize case details using AI."""
    
    def __init__(self):
        self.ai = AIGateway()
    
    def generate_summary(self, case_data: Dict[str, Any], language: str = "English") -> Dict[str, Any]:
        """
        Generate a human-readable summary of case details.
        
        Args:
            case_data: Case details dictionary
            language: Language for summary (English, Hindi, etc.)
        
        Returns:
            Dictionary with summary and provider info
        """
        try:
            # Build prompt
            prompt = self._build_prompt(case_data, language)
            
            # Generate response
            response = self.ai.generate_response(prompt, max_tokens=600)
            
            if response.get("success"):
                return {
                    "success": True,
                    "summary": response.get("response"),
                    "provider": response.get("provider"),
                    "language": language
                }
            else:
                return {
                    "success": False,
                    "error": response.get("response", "AI generation failed")
                }
                
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_prompt(self, case_data: Dict[str, Any], language: str) -> str:
        """Build the prompt for AI."""
        
        case_number = case_data.get("case_number", "N/A")
        case_type = case_data.get("case_type", "N/A")
        cnr = case_data.get("cnr_number", "N/A")
        petitioner = case_data.get("petitioner", "N/A")
        respondent = case_data.get("respondent", "N/A")
        status = case_data.get("status", "Unknown")
        next_hearing = case_data.get("next_hearing", "Not scheduled")
        court = case_data.get("court", "Delhi High Court")
        
        prompt = f"""
You are a legal assistant helping a common person understand their court case. 
Explain the following case in simple, clear language in {language}.

Case Details:
- Case Number: {case_number}
- Case Type: {case_type}
- Court: {court}
- CNR: {cnr}
- Petitioner: {petitioner}
- Respondent: {respondent}
- Status: {status}
- Next Hearing: {next_hearing}

Please provide:
1. A brief summary of what this case is about (2-3 sentences)
2. What the current status means in simple terms
3. What should the party expect next
4. Any important things to note

Use simple language. Avoid legal jargon. If you explain a legal term, explain it in simple words.
Make it easy for a non-lawyer to understand.
"""
        return prompt
    
    def generate_bulk_summary(self, cases: list, language: str = "English") -> list:
        """Generate summaries for multiple cases."""
        results = []
        
        for case in cases:
            summary = self.generate_summary(case, language)
            results.append({
                "case": case,
                "summary": summary
            })
        
        return results