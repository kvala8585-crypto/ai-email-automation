import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(email_text):
    try:
        if not email_text or not email_text.strip():
            return {
                "category": "General",
                "reply": "Empty email content received."
            }

        prompt = f"""
        Classify this email and generate a professional reply.

        Email:
        {email_text}

        Output format:
        Category: <Support/Sales/Spam/Urgent>
        Reply: <response>
        """

        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(prompt)

        if not response or not response.text:
            raise Exception("Empty AI response")

        text = response.text.strip()

        category = "General"
        reply = text

        if "Category:" in text and "Reply:" in text:
            try:
                parts = text.split("Reply:")
                category = parts[0].replace("Category:", "").strip()
                reply = parts[1].strip()
            except:
                pass

        return {
            "category": category,
            "reply": reply
        }

    except Exception as e:
        print("AI ERROR:", e)

        # ✅ fallback
        return {
            "category": "System",
            "reply": "AI service unavailable, fallback response."
        }