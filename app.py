import os
import imaplib
import email
from email.header import decode_header
from google import genai

def fetch_latest_unread():
    IMAP_SERVER = os.environ.get("IMAP_SERVER", "imap.gmail.com")
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    # If credentials aren't even provided, switch to mock mode gracefully
    if not EMAIL_USER or not EMAIL_PASS:
        print("\n[Status]: Missing email credentials. Running in OFFLINE mock mode.")
        return "Mock Email: Hey Ed, welcome back from vacation! Can we sync on the database migration today?"

    try:
        print(f"Connecting to {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        mail_ids = messages[0].split()

        if not mail_ids:
            print("🎉 No unread emails found! Your inbox is clean.")
            return None

        latest_id = mail_ids[-1]
        status, data = mail.fetch(latest_id, "(RFC822)")

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                
                print(f"\n[Inbox Success]: Connected! Reading email: '{subject}'")
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            return part.get_payload(decode=True).decode()
                else:
                    return msg.get_payload(decode=True).decode()
        
        mail.logout()
    except Exception as e:
        # If the credentials are provided but WRONG (like the curly quote issue), catch it here
        print(f"\n❌ [Connection Error]: Could not log in. Details: {e}")
        print("Falling back to simulated email for testing safety...")
        return "Mock Email: Hey Ed, welcome back from vacation! Can we sync on the database migration today?"
    
    return None

def main():
    print("--- AI Inbox Assistant Active ---")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    email_content = fetch_latest_unread()
    if not email_content:
        return

    if not api_key:
        print("\n[Status]: No GEMINI_API_KEY detected. Running AI in mock mode.")
        print("[Mock AI Response]: (Connect your Gemini key to get live summaries and drafts!)")
    else:
        client = genai.Client(api_key=api_key)
        try:
            print("Analyzing email content with Gemini...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"You are an executive assistant. Summarize this email and suggest a professional reply draft: {email_content}"
            )
            print("\n================ AI ANALYSIS ================")
            print(response.text)
            print("=============================================")
        except Exception as e:
            print(f"[Gemini Error]: {e}")

if __name__ == "__main__":
    main()