import os
import json
from openai import OpenAI

class EmailClassifier:
    def __init__(self):
        # Initialize the client using the key from .env
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY in .env file")
        self.client = OpenAI(api_key=api_key)

    def classify(self, email_body):
        """
        Analyzes an email and returns a Category and a 1-sentence summary.
        """
        prompt = f"""
        You are an email routing assistant. 
        Categorize the following email into one of these buckets: [URGENT_SUPPORT, BILLING, SALES_LEAD, SPAM, GENERAL].
        Also provide a very brief summary (max 10 words).
        
        Return a valid JSON object with keys: "category" and "summary".

        Email Content:
        "{email_body}"
        """

        try:
            # We use gpt-4o-mini because it is fast and cheap
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error classifying email: {e}")
            return {"category": "ERROR", "summary": "Could not process"}