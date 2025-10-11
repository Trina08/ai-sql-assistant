import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your GEMINI_API_KEY from the .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("\n🔍 Fetching available Gemini models...\n")

try:
    models = genai.list_models()
    for m in models:
        print("✅", m.name)
    print("\n🎉 Above are all models available to your key!")
except Exception as e:
    print("❌ Error fetching models:", e)
