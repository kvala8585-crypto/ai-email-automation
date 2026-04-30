from fastapi import FastAPI
from backend.email_handler import read_emails, send_email
from backend.ai_handler import generate_reply
from backend.database import SessionLocal, EmailLog

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Email Automation System Running 🚀"}

@app.get("/process-emails")
def process_emails():
    emails = read_emails()
    db = SessionLocal()

    results = []

    for subject, body, sender in emails:
        ai_output = generate_reply(body)

        if isinstance(ai_output, dict):
            category = ai_output.get("category", "General")
            reply = ai_output.get("reply", "No reply generated")
        else:
            try:
                lines = ai_output.split("\n")
                category = lines[0].replace("Category:", "").strip()
                reply = "\n".join(lines[1:]).replace("Reply:", "").strip()
            except:
                category = "Unknown"
                reply = str(ai_output)

        # save DB
        log = EmailLog(
            subject=str(subject),
            category=str(category),
            response=str(reply)
        )
        db.add(log)
        db.commit()

        # ✅ AUTO REPLY SEND
        try:
            send_email(
                to_email=sender,
                subject=f"Re: {subject}",
                body=reply
            )
            email_status = "Reply Sent"
        except Exception as e:
            email_status = f"Send Failed: {str(e)}"

        results.append({
            "subject": subject,
            "category": category,
            "email_status": email_status
        })

    db.close()

    return {
        "status": "success",
        "processed_emails": results
    }