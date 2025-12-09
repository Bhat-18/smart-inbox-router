import imaplib
import email
import os
from email.header import decode_header
from bs4 import BeautifulSoup

class EmailIngestor:
    def __init__(self):
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = "imap.gmail.com"

    def fetch_unread_emails(self, limit=3):
        """
        Connects to Gmail, grabs the latest 'limit' unread emails, 
        and formats them as simple text.
        """
        if not self.username or not self.password:
            print("❌ Missing Email Credentials in .env")
            return []

        print("🔌 Connecting to Gmail...")
        mail = imaplib.IMAP4_SSL(self.imap_server)
        
        try:
            mail.login(self.username, self.password)
            mail.select("inbox")

            # Search for unread emails
            status, messages = mail.search(None, "UNSEEN")
            email_ids = messages[0].split()
            
            # Get the latest ones only
            latest_email_ids = email_ids[-limit:]
            
            cleaned_emails = []

            for e_id in latest_email_ids:
                # Fetch the email
                _, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode Subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        # Get sender
                        sender = msg.get("From")

                        # Get body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        # Combine into a clean block for the LLM
                        full_text = f"From: {sender}\nSubject: {subject}\nBody: {body[:500]}" # Limit body to 500 chars
                        cleaned_emails.append(full_text)

            mail.close()
            mail.logout()
            return cleaned_emails

        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []