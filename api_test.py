import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Suppress noisy logs from the HTTP client
logging.basicConfig(level=logging.ERROR)

# Load environment variables
load_dotenv()

def find_working_model():
    """Connects to Google AI and finds a working model for text generation."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file. Please check the file.")
        return

    try:
        genai.configure(api_key=api_key)
        print("✅ Successfully connected to Google AI.")
        print("🔎 Searching for a model that supports text generation...\n")

        # Find a model that supports the 'generateContent' method
        working_model = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Prefer a 'gemini-pro' model if available
                if 'gemini-1.0-pro' in m.name:
                    working_model = m.name
                    break # Found the best one, stop searching
                elif 'gemini-pro' in m.name:
                    working_model = m.name
                    break
        
        # If no pro model was found, take the first available one
        if not working_model:
             for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    working_model = m.name
                    break

        if working_model:
            # The SDK expects the name without the "models/" prefix
            final_model_name = working_model.replace("models/", "")
            print("🎉 SUCCESS! Found a working model for your API key.")
            print("\n=====================================================================")
            print(f"  Your model name is:  '{final_model_name}'")
            print("=====================================================================")
            print("\nNEXT STEP: Please copy this exact model name into your `email_generator.py` file.")
        else:
            print("❌ CRITICAL ERROR: No models supporting text generation were found for your API key.")
            print("This is highly unusual and suggests an issue with your Google Cloud project's permissions or region.")

    except Exception as e:
        print(f"❌ An error occurred while trying to connect or list models: {e}")
        print("Please ensure your API key is correct and that the 'Generative Language API' is enabled in your Google Cloud project.")

if __name__ == "__main__":
    find_working_model()