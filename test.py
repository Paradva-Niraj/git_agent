# Install required SDK:
# pip install -q -U google-genai

import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Please set the GEMINI_API_KEY environment variable")

# Initialize the Gemini client (auto-picks up GEMINI_API_KEY)
client = genai.Client()
prompt = "Explain how AI works in a few words"
# Generate a short explanation using Gemini‑2.5‑flash
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)
