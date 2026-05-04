#  AI-Powered Email Automation & Smart Response System
##  Overview

This project is an AI-driven email automation system with intelligent fallback handling.

Uses AI (Gemini API) for classification and response generation,

and a rule-based system to ensure uninterrupted automation when API limits are reached.

Built an automated customer support workflow inspired by real-world industry use cases.



## Features

*  Read incoming emails using IMAP (Gmail)
*  AI-based email classification (Support, Sales, Spam, Urgent)
*  Automatic response generation
*  Store processed emails in database (SQLite)
*  FastAPI backend for processing
*  Automation-ready (n8n integration)


##  Tech Stack

* **Backend:** FastAPI (Python)
* **AI Model:** Gemini / OpenAI
* **Database:** SQLite + SQLAlchemy
* **Email Protocols:** IMAP & SMTP
* **Automation:** n8n
* **Deployment:** Render(Cloud Run)http://ai-email-automation-5.onrender.com/

##  Project Structure

```
AI Email Automation & Smart Reply System/
│
├── backend/
│   ├── main.py
│   ├── email_handler.py
│   ├── ai_handler.py
│   ├── database.py
│   ├── requirements.txt
│
├── 
├── README.md

##  Setup Instructions

### 1. Clone Repository

```
git clonehttps://github.com/kvala8585-crypto/ai-email-automation/


### 2. Install Dependencies

```
pip install -r backend/requirements.txt
```

### 3. Setup Environment Variables


## Run Project

```
uvicorn backend.main:app --reload
```

Open:

```
http://127.0.0.1:8000/process-emails
```

---

##  Automation (n8n)

* Create a **Cron Trigger**
* Add **HTTP Request Node**
* Call:

```
http://localhost:8000/process-emails
```

---

##  Deployment (render)

* Use **Cloud Run**
* Deploy using Render

## Future Enhancements

*  Dashboard (Streamlit / React)
*  Attachment parsing (PDF/Docs)
*  Slack/WhatsApp integration
*  Advanced ML spam detection
*  Auto email reply sendig

## Author
kavi vala



Your Name
kavi vala
