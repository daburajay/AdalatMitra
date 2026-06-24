# test_captcha_v2.py - Improved CAPTCHA test with better handling

import os
import sys
import asyncio
import time
from pathlib import Path
from PIL import Image, ImageEnhance

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print(f"HF_TOKEN loaded: {'✅' if os.getenv('HF_TOKEN') else '❌ missing'}")

from bharat_courts import get_court, HCServicesClient
from bharat_courts.captcha.base import CaptchaSolver


class ManualCAPTCHASolver(CaptchaSolver):
    """Manual CAPTCHA solver with improved handling."""
    
    def __init__(self, captcha_answer=None):
        self._answer = captcha_answer
        self._attempt = 0
    
    async def solve(self, image_bytes: bytes) -> str:
        self._attempt += 1
        
        # Save the CAPTCHA image
        captcha_path = "captcha_temp.png"
        with open(captcha_path, "wb") as f:
            f.write(image_bytes)
        
        print(f"\n🔐 CAPTCHA #{self._attempt} saved to: {os.path.abspath(captcha_path)}")
        
        # Try to enhance and display the image
        try:
            img = Image.open(captcha_path)
            # Enhance contrast for better readability
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            img.save("captcha_enhanced.png")
            print("   📸 Enhanced image saved to: captcha_enhanced.png")
            
            # Show the image
            img.show()
            print("   📸 Image opened in default viewer")
        except Exception as e:
            print(f"   ⚠️ Could not enhance image: {e}")
        
        if self._answer:
            print(f"   Using pre-set answer: {self._answer}")
            return self._answer
        
        # Ask user for CAPTCHA
        print("\n📝 Please read the CAPTCHA from the image (5-6 characters):")
        answer = input("   Enter CAPTCHA: ").strip().lower()
        
        if not answer:
            raise Exception("No CAPTCHA entered")
        
        print(f"   ✅ Using CAPTCHA: {answer}")
        return answer


async def search_with_manual_captcha():
    """Search with manual CAPTCHA entry."""
    print("\n" + "=" * 70)
    print("  CAPTCHA Search with Manual Entry")
    print("=" * 70)
    
    COURT = "Delhi High Court"
    court_code = "delhi"
    court = get_court(court_code)
    
    # Step 1: Get CAPTCHA from user
    print("\n📝 Step 1: CAPTCHA required")
    print("   The CAPTCHA image will open automatically.")
    print("   If it doesn't open, check 'captcha_temp.png' in the current directory.")
    
    # Create solver
    solver = ManualCAPTCHASolver()
    
    try:
        async with HCServicesClient(captcha_solver=solver) as client:
            print("\n🔍 Step 2: Searching for cases...")
            print("   Party: Union of India")
            print("   Year: 2024")
            print("   Status: Pending")
            
            result = await client.case_status_by_party(
                court,
                party_name="Union of India",
                year="2024",
                status_filter="Pending",
            )
            
            # Success!
            print("\n" + "=" * 70)
            print("✅ SEARCH SUCCESSFUL!")
            print(f"   Found {len(result) if result else 0} cases")
            
            if result and len(result) > 0:
                print("\n📋 Case Details:")
                first = result[0]
                print(f"   Case Number: {first.case_number}")
                print(f"   Case Type: {first.case_type}")
                print(f"   CNR Number: {first.cnr_number}")
                print(f"   Petitioner: {first.petitioner}")
                print(f"   Respondent: {first.respondent}")
                print(f"   Status: {getattr(first, 'status', 'N/A')}")
                
                # Show all cases
                print(f"\n📋 All {len(result)} cases:")
                for i, case in enumerate(result[:5], 1):
                    print(f"   {i}. {case.case_number} - {case.case_type}")
                
            return result
            
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR:")
        print(f"   {e}")
        
        # Check if it's a CAPTCHA error
        if "CAPTCHA" in str(e) or "captcha" in str(e).lower():
            print("\n💡 CAPTCHA was incorrect. The server rejected it.")
            print("   Common issues:")
            print("   - The CAPTCHA might have expired (they're time-sensitive)")
            print("   - You might have misread a character (0 vs O, 1 vs l, etc.)")
            print("   - Try again with a fresh CAPTCHA image")
        
        import traceback
        print("\n📋 Full error:")
        traceback.print_exc()
        return None


def enhance_captcha_image():
    """Enhance the CAPTCHA image for better readability."""
    captcha_path = "captcha_temp.png"
    
    if not os.path.exists(captcha_path):
        print(f"❌ No CAPTCHA image found at: {captcha_path}")
        return
    
    try:
        # Open and enhance the image
        img = Image.open(captcha_path)
        
        # Convert to grayscale if not already
        if img.mode != 'L':
            img = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(3.0)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        
        # Save enhanced version
        enhanced_path = "captcha_enhanced.png"
        img.save(enhanced_path)
        
        print(f"✅ Enhanced CAPTCHA saved to: {os.path.abspath(enhanced_path)}")
        print("   Open this file for a clearer view of the CAPTCHA")
        
        # Show the image
        img.show()
        
    except Exception as e:
        print(f"❌ Error enhancing image: {e}")


def main():
    print("\n" + "=" * 70)
    print("  CAPTCHA Test Tool")
    print("=" * 70)
    
    print("\n📋 Options:")
    print("  1. Search with manual CAPTCHA (recommended)")
    print("  2. Enhance existing CAPTCHA image for clarity")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(search_with_manual_captcha())
    elif choice == "2":
        enhance_captcha_image()
    else:
        print("Exiting...")
        return
    
    print("\n" + "=" * 70)
    print("  Done!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")