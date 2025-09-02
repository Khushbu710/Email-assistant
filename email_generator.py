import os
from groq import Groq
from dotenv import load_dotenv
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

class EmailGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file. Please get a key from https://console.groq.com/keys")
        
        try:
            self.client = Groq(api_key=self.api_key)
            self.model_name = "llama-3.1-8b-instant" # Using Llama 3 via Groq
            logging.info("Groq client configured successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to configure Groq client: {e}")

    def test_connection(self):
        """Tests the connection to the Groq API."""
        logging.info("Testing connection to Groq...")
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello, world!"}],
                model=self.model_name,
                max_tokens=10,
            )
            if chat_completion.choices[0].message.content:
                logging.info("✅ Groq connection successful!")
                return True, f"Connected successfully to Groq ({self.model_name})"
            else:
                return False, "Connection test failed: Received an empty response."
        except Exception as e:
            logging.error(f"Groq connection error: {e}")
            return False, f"Failed to connect to Groq. Please check your API key and internet connection. Error: {e}"

    def generate_email(self, key_points, recipient, sender, purpose, tone, length):
        """Generate an email using the Groq Llama 3 model."""
        logging.info(f"Generating email with Groq ({self.model_name})...")

        if length == "Short":
            max_tokens = 150
        elif length == "Medium":
            max_tokens = 300
        else: # Long
            max_tokens = 500

        system_prompt = "You are a helpful AI assistant that writes professional, complete, and courteous emails. Always start with an appropriate subject line. Ensure the email includes all requested details and ends with a suitable closing/sign-off. Do not provide explanations or meta-commentary, only the email content itself."

        user_prompt = f"""
        # Write a {tone} email from {sender} to {recipient} about {purpose}.
        # The email should be {length.lower()}.
        
        # Incorporate these key points:
        # - {key_points}
        Write a professional email with the following details:

        - Sender: {sender}
        - Recipient: {recipient}
        - Purpose of the email: {purpose}
        - Tone: {tone}
        - Key points to include: {key_points}

        Begin with a clear subject line ("Subject: ...").
        Structure the email to be well-organized, polite, and complete. Ensure all key points are included and the email ends with a proper closing/sign-off.

        Generate only the full email content.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.model_name,
                max_tokens=max_tokens,
            )
            generated_text = chat_completion.choices[0].message.content
            logging.info("Email generated successfully.")
            return generated_text
        except Exception as e:
            logging.error(f"Error during email generation: {e}")
            raise Exception(f"Failed to generate email using Groq. Error: {e}")

    def improve_email(self, email_text):
        """Suggest improvements for an email using Groq."""
        logging.info("Improving email with Groq...")
        
        prompt = f"""
        Analyze the following email and provide 3-4 specific, actionable suggestions for how to improve it.
        Focus on clarity, tone, and professionalism. Format your suggestions as a bulleted list.

        Email to analyze:
        ---
        {email_text}
        ---

        Suggestions:
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                max_tokens=300,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during email improvement: {e}")
            return f"Failed to get suggestions. Error: {e}"
