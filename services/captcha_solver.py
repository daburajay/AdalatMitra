"""
services/captcha_solver.py - CAPTCHA Solver with Multiple Options
"""

import os
from PIL import Image, ImageEnhance
from bharat_courts.captcha.base import CaptchaSolver
from utils.logger import get_logger
from utils.constants import CAPTCHA_IMAGE_PATH

logger = get_logger("captcha_solver")


# ============================================
# OPTION 1: Direct OCR Solver (EASYOCR) - WORKING
# ============================================

class DirectOCRSolver(CaptchaSolver):
    """OCR solver using EasyOCR - CONFIRMED WORKING"""
    
    def __init__(self):
        self.reader = None
        try:
            import easyocr
            self.reader = easyocr.Reader(['en'], gpu=False)
            logger.info("✅ EasyOCR initialized")
        except ImportError:
            logger.error("❌ easyocr not installed. Run: pip install easyocr")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to initialize EasyOCR: {e}")
            raise
    
    async def solve(self, image_bytes: bytes) -> str:
        # Save for debugging
        with open(CAPTCHA_IMAGE_PATH, "wb") as f:
            f.write(image_bytes)
        
        # Read with EasyOCR
        result = self.reader.readtext(image_bytes, detail=0)
        
        if result:
            text = ''.join(result).replace(' ', '').replace('\n', '')
            logger.info(f"OCR Result: {text}")
            return text
        
        raise Exception("OCR failed to read CAPTCHA")


# ============================================
# OPTION 2: EasyOCR Solver (Alias for DirectOCRSolver)
# ============================================

class EasyOCRCaptchaSolver(DirectOCRSolver):
    """Alias for DirectOCRSolver"""
    pass


# ============================================
# OPTION 3: Tesseract OCR Solver
# ============================================

class TesseractCaptchaSolver(CaptchaSolver):
    """CAPTCHA solver using Tesseract OCR"""
    
    def __init__(self, tesseract_path: str = None):
        self.tesseract_path = tesseract_path
        try:
            import pytesseract
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            self.tesseract = pytesseract
            logger.info("✅ Tesseract initialized")
        except ImportError:
            logger.error("❌ pytesseract not installed. Run: pip install pytesseract")
            raise
    
    def _enhance_image(self, image_path: str) -> str:
        """Enhance image for better OCR"""
        try:
            img = Image.open(image_path)
            if img.mode != 'L':
                img = img.convert('L')
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(3.0)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            
            enhanced_path = "captcha_enhanced.png"
            img.save(enhanced_path)
            return enhanced_path
        except Exception as e:
            logger.warning(f"Could not enhance image: {e}")
            return image_path
    
    async def solve(self, image_bytes: bytes) -> str:
        # Save CAPTCHA image
        with open(CAPTCHA_IMAGE_PATH, "wb") as f:
            f.write(image_bytes)
        
        logger.info(f"CAPTCHA saved to {os.path.abspath(CAPTCHA_IMAGE_PATH)}")
        
        # Enhance the image
        enhanced_path = self._enhance_image(CAPTCHA_IMAGE_PATH)
        
        # Use Tesseract
        custom_config = r'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        
        try:
            text = self.tesseract.image_to_string(enhanced_path, config=custom_config)
            result = text.strip().replace(' ', '').replace('\n', '')
            logger.info(f"Tesseract Result: {result}")
            
            if result and len(result) >= 5:
                return result
            else:
                # Try with original image
                text = self.tesseract.image_to_string(CAPTCHA_IMAGE_PATH, config=custom_config)
                result = text.strip().replace(' ', '').replace('\n', '')
                logger.info(f"Tesseract Result (original): {result}")
                if result and len(result) >= 5:
                    return result
                
                raise Exception(f"OCR failed: Could not read CAPTCHA. Result: '{result}'")
                
        except Exception as e:
            logger.error(f"Tesseract error: {e}")
            raise


# ============================================
# OPTION 4: Manual Entry Solver (Fallback)
# ============================================

class ManualCaptchaSolver(CaptchaSolver):
    """Manual CAPTCHA entry - same as working CLI test"""
    
    def __init__(self, captcha_answer: str = None):
        self._answer = captcha_answer
    
    async def solve(self, image_bytes: bytes) -> str:
        # Save CAPTCHA image
        with open(CAPTCHA_IMAGE_PATH, "wb") as f:
            f.write(image_bytes)
        
        logger.info(f"CAPTCHA saved to {os.path.abspath(CAPTCHA_IMAGE_PATH)}")
        
        # If answer is provided (from UI), use it
        if self._answer:
            answer = self._answer
            self._answer = None
            logger.info(f"Using manual CAPTCHA: {answer}")
            return answer
        
        # No answer - raise for UI to handle
        raise Exception("CAPTCHA_REQUIRED")


# ============================================
# OPTION 5: Hybrid Solver (Try OCR First, Fallback to Manual)
# ============================================

class HybridCaptchaSolver(CaptchaSolver):
    """Try EasyOCR first, fallback to manual entry"""
    
    def __init__(self, captcha_answer: str = None):
        self._answer = captcha_answer
        self._ocr_solver = None
        
        # Try to initialize EasyOCR first
        try:
            self._ocr_solver = DirectOCRSolver()
            logger.info("✅ Hybrid solver using EasyOCR")
        except:
            logger.warning("⚠️ No OCR available, using manual only")
    
    async def solve(self, image_bytes: bytes) -> str:
        # Save CAPTCHA image
        with open(CAPTCHA_IMAGE_PATH, "wb") as f:
            f.write(image_bytes)
        
        logger.info(f"CAPTCHA saved to {os.path.abspath(CAPTCHA_IMAGE_PATH)}")
        
        # Try OCR first if available
        if self._ocr_solver:
            try:
                return await self._ocr_solver.solve(image_bytes)
            except Exception as e:
                logger.warning(f"OCR failed: {e}. Falling back to manual.")
        
        # Fallback to manual entry
        if self._answer:
            answer = self._answer
            self._answer = None
            logger.info(f"Using manual CAPTCHA: {answer}")
            return answer
        
        # No answer - raise for UI to handle
        raise Exception("CAPTCHA_REQUIRED")