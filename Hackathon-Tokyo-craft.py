import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=api_key)

try:
    # Use gemini-pro-latest which was confirmed in the list
    model_name = 'models/gemini-pro-latest'
    print(f"Attempting to use: {model_name}")
    
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello! This is a test from Hackathon-Tokyo-craft. Please reply with 'Gemini is ready!' if you can hear me.")
    
    print("-" * 30)
    print("Gemini API Response:")
    print(response.text)
    print("-" * 30)
    print("Verification Successful!")
    
except Exception as e:
    print("-" * 30)
    print("Verification Failed!")
    print(f"Error: {e}")
    print("-" * 30)
