import streamlit as st
import requests

# Backend URL (local or deployed)
BACKEND_URL = "http://127.0.0.1:8000/process-emails"

st.set_page_config(page_title="AI Email Automation", page_icon="📧")

st.title("📧 AI Email Automation System")
st.write("Click below to process emails and send auto replies")

# Button to trigger backend
if st.button("🚀 Process Emails"):

    with st.spinner("Processing emails..."):

        try:
            response = requests.get(BACKEND_URL)

            if response.status_code == 200:
                data = response.json()

                st.success("✅ Emails processed successfully!")

                emails = data.get("processed_emails", [])

                if not emails:
                    st.warning("📭 No emails found")
                else:
                    for email in emails:
                        st.subheader(f"📌 Subject: {email.get('subject', '')}")
                        st.write(f"📂 Category: {email.get('category', '')}")
                        st.write(f"📤 Status: {email.get('email_status', '')}")
                        st.markdown("---")

            else:
                st.error(f"❌ Server Error: {response.status_code}")

        except Exception as e:
            st.error(f"❌ Connection Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Built with FastAPI + Streamlit 🚀")