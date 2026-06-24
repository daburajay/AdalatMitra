# agents/testp.py
print("Script started...")

import asyncio
import os
import json
from dotenv import load_dotenv

load_dotenv()
print(f"HF_TOKEN loaded: {'✅ Yes' if os.getenv('HF_TOKEN') else '❌ No'}")

from bharat_courts import get_court, HCServicesClient
from bharat_courts.captcha.base import CaptchaSolver


class PrintCaptchaSolver(CaptchaSolver):
    async def solve(self, image_bytes: bytes) -> str:
        captcha_path = os.path.abspath("captcha_temp.png")
        with open(captcha_path, "wb") as f:
            f.write(image_bytes)
        print(f"\n🔐 CAPTCHA saved → {captcha_path}")
        print("   Open File Explorer → your project folder → captcha_temp.png")
        print("   Read the characters and type below (take your time):")
        answer = input("   CAPTCHA answer: ").strip()
        return answer


async def main():
    print("\n" + "=" * 55)
    print("  AdalatMitra — Live eCourts Data Test")
    print("=" * 55)

    court = get_court("delhi")
    solver = PrintCaptchaSolver()
    print(f"Court  : {court.name}")

    # Variables shared across tests
    case_types_dict = {}  # {id: name}
    cases = []
    orders = []
    real_case_type = ""
    real_case_num = ""
    real_year = ""

    async with HCServicesClient(captcha_solver=solver) as client:

        # ── TEST 1: Get case types (no CAPTCHA) ────────────────
        print("\n── TEST 1: Fetching case types for Delhi HC...")
        print("  No CAPTCHA needed here.\n")
        try:
            raw = await client.list_case_types(court)

            # raw is a dict: {"134": "W.P.(C)", "135": "W.P.(CRL)", ...}
            # or a list — let's handle both
            if isinstance(raw, dict):
                case_types_dict = raw
            elif isinstance(raw, list):
                # list of objects with .id and .name
                case_types_dict = {str(ct.id): ct.name for ct in raw}
            else:
                print(f"  Unexpected type: {type(raw)} — raw value: {raw}")
                return

            print(f"✅ Found {len(case_types_dict)} case types. First 10:\n")
            print(f"  {'ID':<10} Case Type Name")
            print(f"  {'-'*45}")

            count = 0
            for ct_id, ct_name in case_types_dict.items():
                if count >= 10:
                    break
                print(f"  {str(ct_id):<10} {ct_name}")
                count += 1

            print(f"\n  ... and {len(case_types_dict) - 10} more.")

            # Auto-find WP(C) ID
            for ct_id, ct_name in case_types_dict.items():
                if "W.P.(C)" in str(ct_name) or "WP(C)" in str(ct_name):
                    print(f"\n  → W.P.(C) ID on Delhi HC: {ct_id}")
                    break

            # Use first key as default for later tests
            real_case_type = list(case_types_dict.keys())[0]
            print(f"  → Using case type '{real_case_type}' for Test 3")

        except Exception as e:
            print(f"❌ Test 1 failed: {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()
            return

        # ── TEST 2: Search by party name (CAPTCHA HERE) ────────
        print("\n── TEST 2: Searching by party name...")
        print("  Party  : 'Union of India'")
        print("  Year   : 2024")
        print("  Status : Pending")
        print("\n  ⚠️  CAPTCHA will appear after you press ENTER.")
        print("  The image saves to captcha_temp.png in your project folder.")
        print("  Open it, read the text, type it when asked.\n")
        input("  Press ENTER when ready → ")

        try:
            cases = await client.case_status_by_party(
                court,
                party_name="Union of India",
                year="2024",
                status_filter="Pending",
            )

            if not cases:
                print("❌ No cases found.")
                return

            print(f"\n✅ Found {len(cases)} case(s). Showing first 3:\n")

            count = 0
            for case in cases:
                if count >= 3:
                    break
                print(f"  [{count+1}] Case Number : {case.case_number}")
                print(f"       Case Type  : {case.case_type}")
                print(f"       CNR        : {case.cnr_number}")
                print(f"       Petitioner : {case.petitioner}")
                print(f"       Respondent : {case.respondent}")
                print()
                count += 1

            # Extract values for Test 3
            first = cases[0]
            raw_num = str(first.case_number or "")
            real_year = raw_num.split("/")[-1].strip() if "/" in raw_num else "2024"
            real_case_num = raw_num.split("/")[0].strip() if "/" in raw_num else raw_num

            print(f"  → Extracted for Test 3:")
            print(f"     case_type = {real_case_type}")
            print(f"     number    = {real_case_num}")
            print(f"     year      = {real_year}")

        except Exception as e:
            print(f"❌ Test 2 failed: {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()
            return

        # ── TEST 3: Search by case number (CAPTCHA HERE) ───────
        print("\n── TEST 3: Fetching case by number...")
        print(f"  case_type = {real_case_type}")
        print(f"  number    = {real_case_num}")
        print(f"  year      = {real_year}")
        print("\n  ⚠️  Another CAPTCHA may appear.\n")
        input("  Press ENTER when ready → ")

        try:
            case_details = await client.case_status(
                court,
                case_type=real_case_type,
                case_number=real_case_num,
                year=real_year,
            )

            if not case_details:
                print("❌ Case not found.")
            else:
                c = case_details[6]
                print(f"\n✅ Case found!\n")
                print(f"  Case Type     : {c.case_type}")
                print(f"  Case Number   : {c.case_number}")
                print(f"  CNR Number    : {c.cnr_number}")
                print(f"  Filing Number : {c.filing_number}")
                print(f"  Petitioner    : {c.petitioner}")
                print(f"  Respondent    : {c.respondent}")
                print(f"  Court         : {c.court_name}")
                print(f"  Status        : {c.status or 'N/A'}")
                print(f"  Next Hearing  : {c.next_hearing_date or 'N/A'}")

        except Exception as e:
            print(f"❌ Test 3 failed: {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()

        # ── TEST 4: Fetch orders ────────────────────────────────
        print("\n── TEST 4: Fetching orders...")

        try:
            orders = await client.court_orders(
                court,
                case_type=real_case_type,
                case_number=real_case_num,
                year=real_year,
            )

            if not orders:
                print("  No orders found.")
            else:
                print(f"✅ Found {len(orders)} order(s):\n")
                count = 0
                for order in orders:
                    if count >= 5:
                        break
                    print(f"  [{count+1}] Date  : {order.order_date}")
                    print(f"       Type  : {order.order_type}")
                    print(f"       Judge : {order.judge}")
                    print()
                    count += 1

        except Exception as e:
            print(f"❌ Test 4 failed: {type(e).__name__}: {e}")

        # ── SAVE to JSON ────────────────────────────────────────
        print("\n── Saving to case_output.json...")
        try:
            output = {
                "court": court.name,
                "case_types": case_types_dict,
                "cases_found": [c.to_dict(exclude_none=True) for c in cases[:3]],
                "orders": [o.to_dict(exclude_none=True) for o in orders],
            }
            with open("case_output.json", "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False, default=str)
            print("✅ Saved to case_output.json")
        except Exception as e:
            print(f"❌ Could not save JSON: {e}")

        print("\n" + "=" * 55)
        print("  All tests done. Check case_output.json for full data.")
        print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
