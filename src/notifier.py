import requests
import os
import json

class SlackNotifier:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_alert(self, email_data):
        """
        Sends a formatted message to Slack.
        """
        if not self.webhook_url:
            print("❌ No Slack Webhook URL found. Check your .env file.")
            return

        # Emoji mapping for visual clarity
        emojis = {
            "URGENT_SUPPORT": "🔴",
            "BILLING": "💰",
            "SALES_LEAD": "🚀",
            "SPAM": "🗑️",
            "GENERAL": "📫",
            "ERROR": "⚠️"
        }

        category = email_data.get('category', 'GENERAL')
        icon = emojis.get(category, "❓")
        summary = email_data.get('summary', 'No summary provided')

        # This defines how the message looks in Slack
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{icon} New Inbox Item: {category}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Summary:* {summary}"
                    }
                },
                {
                    "type": "divider"
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 200:
                print(f"Failed to send to Slack: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Network error sending to Slack: {e}")