import os
from dotenv import load_dotenv
from classifier import EmailClassifier
from notifier import SlackNotifier
from ingestor import EmailIngestor

# 1. Load Environment Variables
load_dotenv() 

def main():
    print("🚀 Starting Smart Inbox Router (Production Mode)...")
    
    # Initialize our classes
    brain = EmailClassifier()
    hands = SlackNotifier()
    ear = EmailIngestor()

    # Step 1: Fetch Real Emails
    print("📥 Checking for unread emails...")
    incoming_emails = ear.fetch_unread_emails(limit=3)

    if not incoming_emails:
        print("No new unread emails found.")
        return

    print(f"Found {len(incoming_emails)} emails to process.\n")

    for email_text in incoming_emails:
        print("------------------------------------------------")
        # Step 2: Classify
        result = brain.classify(email_text)
        category = result.get('category')
        print(f"Subject: {email_text.splitlines()[1]}") # Print subject for log
        print(f" -> Analyzed as: {category}")
        
        # Step 3: Notify
        if category != "SPAM":
            hands.send_alert(result)
            print(" -> ✅ Notification sent to Slack.")
        else:
            print(" -> 🗑️ Skipped (Spam)")
            
    print("\n✅ Batch processing complete.")

if __name__ == "__main__":
    main()