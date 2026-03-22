import os
from dotenv import load_dotenv
from google import genai

# Load key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

print(f"--- Checking API Key: {API_KEY[:5]}...{API_KEY[-5:] if API_KEY else 'NONE'} ---")

try:
    client = genai.Client(api_key=API_KEY)
    
    # Test 1: List accessible models
    print("\n1. Accessible Models:")
    models = client.models.list()
    found_2_0 = False
    for m in models:
        print(f" - {m.name}")
        if "gemini-2.0-flash" in m.name:
            found_2_0 = True
            
    # Test 2: Simple Text Prompt
    print("\n2. Testing Simple Response...")
    test_model = 'gemini-2.5-flash' if found_2_0 else 'gemini-1.5-flash'
    response = client.models.generate_content(
        model=test_model,
        contents="Hello! If you can read this, my API key is working. Reply with 'OK'."
    )
    print(f"Result: {response.text}")
    print("\n✅ API KEY IS VALID!")

except Exception as e:
    print(f"\n❌ API CHECK FAILED!")
    print(f"Error Details: {e}")