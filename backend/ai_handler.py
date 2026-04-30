from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(email_text):
    try:
        # ✅ Input validation
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

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        # ✅ Response safety
        if not response or not hasattr(response, "text") or not response.text:
            raise Exception("Empty AI response")

        text = response.text.strip()

        # ✅ Safe parsing
        category = "General"
        reply = text

        if "Category:" in text and "Reply:" in text:
            try:
                parts = text.split("Reply:")
                category_part = parts[0]
                reply_part = parts[1]

                category = category_part.replace("Category:", "").strip()
                reply = reply_part.strip()

                if not category:
                    category = "General"
                if not reply:
                    reply = text

            except:
                pass

        return {
            "category": category,
            "reply": reply
        }

    except Exception as e:
        print("AI ERROR:", e)

        # ✅ SMART FALLBACK (UPGRADED)
        text = email_text.lower()

        if any(word in text for word in ["project", "meeting", "deadline"]):
            category = "Work"
            reply = "Thank you for your email regarding the project. I will review it and get back to you soon."

        elif any(word in text for word in ["urgent", "asap", "important"]):
            category = "Urgent"
            reply = "We have received your urgent request and will respond as soon as possible."

        elif any(word in text for word in ["buy", "price", "cost", "purchase"]):
            category = "Sales"
            reply = "Thank you for your interest. Our team will share pricing details with you shortly."

        elif any(word in text for word in ["help", "issue", "problem", "error"]):
            category = "Support"
            reply = "We’re sorry for the inconvenience. Our support team will assist you shortly."

        elif any(word in text for word in ["ai", "what is", "information"]):
            category = "General Inquiry"
            reply = "Thank you for your query. We will provide you with the requested information soon."

        elif "test" in text:
            category = "Testing"
            reply = "This is a test email response."

        else:
            category = "General"
            reply = "Thank you for your email. We will get back to you shortly."

        return {
            "category": category,
            "reply": reply
        }