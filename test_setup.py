"""
test_setup.py
Test script to verify project setup
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_environment():
    """Test if environment variables are loaded."""
    print("=" * 50)
    print("Testing Environment Setup")
    print("=" * 50)

    # Check API keys
    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    hf_token = os.getenv("HF_TOKEN")

    print(f"GEMINI_API_KEY: {'✅' if gemini_key else '❌ Missing'}")
    print(f"GROQ_API_KEY: {'✅' if groq_key else '❌ Missing'}")
    print(f"HF_TOKEN: {'✅' if hf_token else '❌ Missing'}")

    return bool(gemini_key and groq_key)


def test_imports():
    """Test if all imports work."""
    print("\n" + "=" * 50)
    print("Testing Imports")
    print("=" * 50)

    try:
        from config.settings import GEMINI_API_KEY, GROQ_API_KEY

        print("✅ Settings imported")
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        return False

    try:
        from services.ai_gateway import AIGateway

        print("✅ AIGateway imported")
    except Exception as e:
        print(f"❌ AIGateway import failed: {e}")
        return False

    try:
        from utils.logger import get_logger

        print("✅ Logger imported")
    except Exception as e:
        print(f"❌ Logger import failed: {e}")
        return False

    return True


def test_ai_gateway():
    """Test AI Gateway."""
    print("\n" + "=" * 50)
    print("Testing AI Gateway")
    print("=" * 50)

    try:
        from services.ai_gateway import AIGateway

        ai = AIGateway()

        response = ai.generate_response("Say 'Hello World' in one sentence")

        if response.get("success"):
            print(f"✅ AI Gateway working")
            print(f"   Provider: {response.get('provider')}")
            print(f"   Response: {response.get('response')[:100]}...")
        else:
            print(f"❌ AI Gateway failed: {response.get('response')}")
            return False
    except Exception as e:
        print(f"❌ AI Gateway test failed: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("\n🚀 Testing AdalatMitra Setup")
    print("=" * 50)

    # Test 1: Environment
    env_ok = test_environment()

    # Test 2: Imports
    imports_ok = test_imports()

    # Test 3: AI Gateway
    ai_ok = test_ai_gateway()

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"AI Gateway: {'✅' if ai_ok else '❌'}")

    if all([env_ok, imports_ok, ai_ok]):
        print("\n✅ All tests passed! Ready to build the UI.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
