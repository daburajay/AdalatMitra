# test_captcha_fixed.py - Simplified CAPTCHA test

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print(f"HF_TOKEN loaded: {'✅' if os.getenv('HF_TOKEN') else '❌ missing'}")

from services.bharat_court_service import fetch_cases_by_party, fetch_case_types

def get_captcha_answer():
    """Get CAPTCHA answer from user."""
    captcha_path = os.path.abspath("captcha_temp.png")
    print(f"\n🔐 CAPTCHA image saved to: {captcha_path}")
    print("   Open the file and read the CAPTCHA characters")
    print("   (Usually 5-6 characters, case insensitive)")
    return input("\n   Enter CAPTCHA: ").strip()

def test_simple():
    """Simple test with clear output."""
    print("\n" + "=" * 60)
    print("  CAPTCHA Test - Simple Mode")
    print("=" * 60)
    
    COURT = "Delhi High Court"
    
    # Step 1: Get case types (no CAPTCHA)
    print("\n📋 Step 1: Fetching case types...")
    try:
        case_types = fetch_case_types(COURT)
        print(f"✅ Found {len(case_types)} case types")
    except Exception as e:
        print(f"❌ Error fetching case types: {e}")
        return
    
    # Step 2: Search by party
    print("\n🔍 Step 2: Searching for 'Union of India' cases...")
    print("   This will require a CAPTCHA")
    
    # First attempt with no CAPTCHA
    result = fetch_cases_by_party(
        court_name=COURT,
        party_name="Union of India",
        year="2024",
        status_filter="Pending",
    )
    
    # Check if CAPTCHA is required
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        # If we need CAPTCHA and it's not provided yet
        if not result.get("success") and result.get("captcha_required"):
            print(f"\n⚠️ CAPTCHA required (attempt {attempt + 1}/{max_attempts})")
            captcha = get_captcha_answer()
            
            if not captcha:
                print("❌ No CAPTCHA entered. Exiting.")
                return
            
            print(f"\n🔄 Retrying with CAPTCHA: {captcha}")
            result = fetch_cases_by_party(
                court_name=COURT,
                party_name="Union of India",
                year="2024",
                status_filter="Pending",
                captcha_answer=captcha,
            )
            
            if result.get("success"):
                break
            else:
                print(f"❌ Attempt {attempt + 1} failed: {result.get('error', 'Unknown error')}")
                attempt += 1
                
                if attempt >= max_attempts:
                    print("\n❌ Max attempts reached. Please try again later.")
                    return
        else:
            # No CAPTCHA needed or already handled
            break
    
    # Show results
    print("\n" + "=" * 60)
    if result.get("success"):
        total = result.get("total", 0)
        print(f"✅ Success! Found {total} case(s)")
        
        cases = result.get("cases", [])
        if cases:
            print("\n📋 First 3 cases:")
            for i, case in enumerate(cases[:3], 1):
                print(f"   {i}. {case.get('case_number', 'N/A')}")
                print(f"      Type: {case.get('case_type', 'N/A')}")
                print(f"      CNR: {case.get('cnr_number', 'N/A')}")
                print()
        else:
            print("   No cases found")
    else:
        print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
    
    print("=" * 60)

def test_auto_mode():
    """Test auto CAPTCHA mode."""
    print("\n" + "=" * 60)
    print("  CAPTCHA Test - Auto Mode")
    print("=" * 60)
    
    COURT = "Delhi High Court"
    
    print("\n📋 Fetching case types...")
    try:
        case_types = fetch_case_types(COURT)
        print(f"✅ Found {len(case_types)} case types")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n🔍 Searching with auto CAPTCHA...")
    result = fetch_cases_by_party(
        court_name=COURT,
        party_name="Union of India",
        year="2024",
        status_filter="Pending",
        # No captcha_answer - will try ONNX first
    )
    
    print("\n" + "=" * 60)
    if result.get("success"):
        print(f"✅ Found {result.get('total', 0)} cases")
        cases = result.get("cases", [])
        if cases:
            print(f"\n📋 First case: {cases[0].get('case_number', 'N/A')}")
    elif result.get("captcha_required"):
        print("⚠️ Auto CAPTCHA failed. Manual entry required.")
        print("   Run the simple test option instead.")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
    print("=" * 60)

def main():
    """Main function."""
    print("\n" + "=" * 60)
    print("  Bharat Court CAPTCHA Test")
    print("=" * 60)
    
    print("\nSelect test mode:")
    print("  1. Simple test (manual CAPTCHA entry)")
    print("  2. Auto test (tries ONNX first)")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_simple()
    elif choice == "2":
        test_auto_mode()
    else:
        print("Exiting...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")