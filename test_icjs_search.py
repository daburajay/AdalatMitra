"""
test_icjs_search.py - Search for ICJS Data in District Courts
"""

import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from bharat_courts import DistrictCourtClient
from bharat_courts.districtcourts.parser import parse_complex_value

load_dotenv()

print(f"HF_TOKEN loaded: {'✅' if os.getenv('HF_TOKEN') else '❌ Not found'}")


class ManualCaptchaSolver:
    async def solve(self, image_bytes: bytes) -> str:
        captcha_path = os.path.abspath("captcha_temp.png")
        with open(captcha_path, "wb") as f:
            f.write(image_bytes)
        print(f"\n🔐 CAPTCHA saved → {captcha_path}")
        print("   Open File Explorer → your project folder → captcha_temp.png")
        answer = input("   CAPTCHA answer: ").strip()
        return answer


async def search_district_case(state_code, district_code, complex_key, party_name, year):
    """Search for a case in a district court and check ICJS data."""
    
    print(f"\n🔍 Searching District Court:")
    print(f"   State: {state_code}")
    print(f"   District: {district_code}")
    print(f"   Complex Key: {complex_key}")
    print(f"   Party: {party_name}")
    print(f"   Year: {year}")
    print("-" * 50)
    
    try:
        # Parse complex key
        code, ests, needs_est = parse_complex_value(complex_key)
        est = ests[0] if needs_est and ests else ""
        
        print(f"   Court Complex Code: {code}")
        print(f"   Est Code: {est if est else 'N/A'}")
        
        solver = ManualCaptchaSolver()
        
        async with DistrictCourtClient(captcha_solver=solver) as client:
            # Search for cases
            cases = await client.case_status_by_party(
                state_code=state_code,
                dist_code=district_code,
                court_complex_code=code,
                est_code=est,
                party_name=party_name,
                year=year
            )
            
            if cases:
                print(f"\n   ✅ Found {len(cases)} cases")
                print("\n   📋 Case Details (with ICJS check):")
                print("   " + "=" * 60)
                
                for i, case in enumerate(cases[:5], 1):
                    print(f"\n   Case {i}:")
                    print(f"      Case Number: {case.case_number}")
                    print(f"      Case Type: {case.case_type}")
                    print(f"      CNR: {case.cnr_number}")
                    print(f"      Petitioner: {case.petitioner}")
                    print(f"      Respondent: {case.respondent}")
                    print(f"      Status: {getattr(case, 'status', 'N/A')}")
                    
                    # Check for ICJS fields
                    print(f"\n      🔍 ICJS Data Check:")
                    icjs_fields = {
                        'fir_number': 'FIR Number',
                        'chargesheet_number': 'Chargesheet Number',
                        'police_station': 'Police Station',
                        'section': 'IPC Sections',
                        'act': 'Act',
                        'accused': 'Accused',
                        'victim': 'Victim',
                        'investigating_officer': 'Investigating Officer',
                        'fir_date': 'FIR Date',
                        'arrest_date': 'Arrest Date'
                    }
                    
                    found_icjs = False
                    for field, label in icjs_fields.items():
                        value = getattr(case, field, None)
                        if value:
                            print(f"         ✅ {label}: {value}")
                            found_icjs = True
                    
                    if not found_icjs:
                        print(f"         ❌ No ICJS data found in this case")
                    
                    # Try to get orders
                    try:
                        orders = await client.court_orders(
                            state_code=state_code,
                            dist_code=district_code,
                            court_complex_code=code,
                            est_code=est,
                            case_type=case.case_type,
                            case_number=case.case_number,
                            year=year
                        )
                        if orders:
                            print(f"\n      📄 Orders available: {len(orders)}")
                            for order in orders[:2]:
                                print(f"         - {order.order_date}: {order.order_type}")
                    except Exception as e:
                        print(f"      ⚠️ Could not fetch orders: {e}")
                
                return cases
            else:
                print(f"\n   ❌ No cases found for {party_name} in year {year}")
                return []
                
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return []


async def search_icjs_data():
    """Search for ICJS data in various district courts."""
    
    print("\n" + "=" * 70)
    print("  🔍 ICJS Data Search in District Courts")
    print("=" * 70)
    
    # Configuration for different states
    # Use the complex keys discovered from the previous test
    search_configs = [
        # Bihar - Patna
        {
            "state_code": "8",
            "district_code": "1",  # Patna
            "complex_key": "1080060@1,2,3,4@Y",  # From discovery
            "name": "Patna District Court",
            "party": "Kumar",
            "year": "2024"
        },
        # Delhi - Tis Hazari
        {
            "state_code": "7",
            "district_code": "1",  # Delhi
            "complex_key": "1070001@2,3,4,5,6,7,8,9,10,11@Y",  # From discovery
            "name": "Tis Hazari Court, Delhi",
            "party": "State",
            "year": "2024"
        },
        # Maharashtra - Mumbai
        {
            "state_code": "27",
            "district_code": "1",  # Mumbai
            "complex_key": "1270001@1,2,3@N",  # From discovery
            "name": "Mumbai District Court",
            "party": "State",
            "year": "2024"
        },
        # Karnataka - Bangalore
        {
            "state_code": "29",
            "district_code": "1",  # Bangalore
            "complex_key": "1290005@1,2,3,4,5@N",  # From discovery
            "name": "Bangalore District Court",
            "party": "State",
            "year": "2024"
        }
    ]
    
    results = []
    
    for config in search_configs:
        print(f"\n📋 Testing: {config['name']}")
        print("=" * 60)
        
        cases = await search_district_case(
            state_code=config['state_code'],
            district_code=config['district_code'],
            complex_key=config['complex_key'],
            party_name=config['party'],
            year=config['year']
        )
        
        if cases:
            results.append({
                "court": config['name'],
                "cases_found": len(cases),
                "icjs_data_found": False,
                "sample_case": cases[0] if cases else None
            })
        
        # Brief pause between requests
        await asyncio.sleep(2)
    
    return results


async def interactive_search():
    """Interactive search for district court cases."""
    
    print("\n" + "=" * 70)
    print("  🔍 Interactive District Court Search")
    print("=" * 70)
    
    # Get inputs
    state_code = input("\nEnter State Code (e.g., 8 for Bihar, 7 for Delhi): ").strip()
    if not state_code:
        print("State code required")
        return
    
    district_code = input("Enter District Code (e.g., 1): ").strip()
    if not district_code:
        print("District code required")
        return
    
    complex_key = input("Enter Complex Key (from discovery): ").strip()
    if not complex_key:
        print("Complex key required")
        return
    
    party_name = input("Enter Party Name (e.g., Kumar, State): ").strip()
    if not party_name:
        party_name = "State"
    
    year = input("Enter Year (default: 2024): ").strip()
    if not year:
        year = "2024"
    
    # Search
    cases = await search_district_case(
        state_code=state_code,
        district_code=district_code,
        complex_key=complex_key,
        party_name=party_name,
        year=year
    )
    
    return cases


async def test_with_known_fir():
    """Test with known FIR/criminal cases."""
    
    print("\n" + "=" * 70)
    print("  🔍 Testing Known Criminal Cases (ICJS Check)")
    print("=" * 70)
    
    print("""
    💡 For testing ICJS data, try cases with:
    - Criminal matters (with FIR numbers)
    - Cases from police stations
    - Cases where chargesheet has been filed
    
    Suggested searches:
    - State of Bihar vs [Accused Name]
    - State vs [Accused Name]
    - [Police Station Name] vs [Accused]
    """)
    
    # Example searches
    test_searches = [
        {"state": "8", "district": "1", "complex": "1080060@1,2,3,4@Y", "party": "State", "year": "2024"},
        {"state": "7", "district": "1", "complex": "1070001@2,3,4,5,6,7,8,9,10,11@Y", "party": "State", "year": "2024"},
    ]
    
    for search in test_searches:
        cases = await search_district_case(
            state_code=search["state"],
            district_code=search["district"],
            complex_key=search["complex"],
            party_name=search["party"],
            year=search["year"]
        )


async def main():
    """Main function."""
    
    print("\n📋 Choose option:")
    print("  1. Search ICJS Data (Pre-configured courts)")
    print("  2. Interactive Search (Custom inputs)")
    print("  3. Test Known Criminal Cases")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        results = await search_icjs_data()
        if results:
            print("\n" + "=" * 70)
            print("  📊 ICJS Data Search Results")
            print("=" * 70)
            for r in results:
                print(f"\n   Court: {r['court']}")
                print(f"      Cases Found: {r['cases_found']}")
                print(f"      ICJS Data: {'✅ Found' if r.get('icjs_data_found') else '❌ Not Found'}")
    
    elif choice == "2":
        await interactive_search()
    
    elif choice == "3":
        await test_with_known_fir()
    
    else:
        print("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())