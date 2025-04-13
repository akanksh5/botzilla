import os
import httpx
from dotenv import load_dotenv

load_dotenv()  # Load SLACK_BOT_TOKEN from .env file

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"

def send_message(channel_id, message_text):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel_id,  # can be a user ID or channel ID like 'C12345678'
        "text": message_text
    }

    response = httpx.post(SLACK_API_URL, json=payload, headers=headers)
    print(response.status_code, response.json())

# Example usage
send_message(CHANNEL_ID, "Hey! This is a test from your bot 🤖")
