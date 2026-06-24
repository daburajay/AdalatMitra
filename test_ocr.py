import asyncio
import os
from dotenv import load_dotenv
from bharat_courts import get_court, HCServicesClient
from bharat_courts.captcha.base import CaptchaSolver
import easyocr
from PIL import Image
import io

load_dotenv()


class DirectOCRSolver(CaptchaSolver):
    """Direct OCR solver for testing"""

    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=False)
        print("✅ EasyOCR initialized")

    async def solve(self, image_bytes: bytes) -> str:
        # Save for debugging
        with open("captcha_test.png", "wb") as f:
            f.write(image_bytes)

            # Read with EasyOCR
            result = self.reader.readtext(image_bytes, detail=0)

            if result:
                text = "".join(result).replace(" ", "").replace("\n", "")
                print(f"📖 OCR Result: {text}")
                return text

            raise Exception("OCR failed")


async def main():
    print("\n🔍 Testing OCR with Bharat Courts API...")
    print("=" * 50)

    court = get_court("delhi")
    solver = DirectOCRSolver()

    async with HCServicesClient(captcha_solver=solver) as client:
        try:
            print("\n📋 Searching for 'Union of India' cases...")
            cases = await client.case_status_by_party(
                court, party_name="Union of India", year="2024", status_filter="Pending"
            )

            if cases:
                print(f"\n✅ Found {len(cases)} cases!")
                print(f"\n📋 First case:")
                first = cases[0]
                print(f"   Case Number: {first.case_number}")
                print(f"   Case Type: {first.case_type}")
                print(f"   Petitioner: {first.petitioner}")
                print(f"   Respondent: {first.respondent}")
            else:
                print("\n❌ No cases found")

        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
