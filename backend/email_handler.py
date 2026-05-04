import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def read_emails():
    try:
        if not EMAIL_USER or not EMAIL_PASS:
            print("❌ Email credentials missing")
            return []

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)

        #  FIX 1: Use All Mail (Gmail specific)
        mail.select('"[Gmail]/All Mail"')

        #  You can switch between ALL / UNSEEN
        status, messages = mail.search(None, "ALL")

        if status != "OK":
            print("❌ Failed to fetch emails")
            return []

        email_ids = messages[0].split()

        print("📩 TOTAL EMAILS FOUND:", len(email_ids))  #  debug

        emails = []

        # FIX 2: last 5 emails (correct slicing)
        for e_id in email_ids[-5:]:
            status, msg_data = mail.fetch(e_id, "(RFC822)")

            if status != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject = msg.get("subject", "")

                    # Clean sender email
                    raw_sender = msg.get("From", "")
                    sender = parseaddr(raw_sender)[1]

                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                                except:
                                    body = ""
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                        except:
                            body = ""

                    emails.append((subject, body, sender))

        mail.logout()
        return emails

    except Exception as e:
        print("❌ EMAIL READ ERROR:", e)
        return []


def send_email(to_email, subject, body):
    try:
        if not EMAIL_USER or not EMAIL_PASS:
            print("❌ Email credentials missing")
            return False

        if not to_email:
            print("❌ Invalid recipient email")
            return False

        msg = MIMEText(body)
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        print("❌ EMAIL SEND ERROR:", e)
        return False
