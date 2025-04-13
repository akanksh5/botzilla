from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import httpx
import random

load_dotenv()

app = FastAPI()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")  



@app.post("/slack/events")
async def slack_events(request: Request):
    content_type = request.headers.get("Content-Type", "")
    if content_type == "application/json":
        body = await request.json()

    # ✅ Step 1: Handle Slack URL verification
        if body.get("type") == "url_verification":
            return {"challenge": body.get("challenge")}
    
    form = await request.form()
    print(form.get("command"))
    user = form.get("user_id")
    if form.get("command") == "/breathe":
        images = ["https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWY5bjZpZXBjM2hlYzB5dHp1MnQ5eG1rZjhvZHJ2aDQ4azRqYTlpZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/krP2NRkLqnKEg/giphy.gif",
                  "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVzY28zdzJ0cjF2czI1anExcWtiYzZqbXh1MjlkMmVrYnd5ZHM2bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/grlsjMsVr2QDPBSNJM/giphy.gif",
                  "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWw3bzQ1NW54ZXBseWRzdXhieHd2aWh1ZGc4cTV0bm0xODI0N3F2OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1xVc4s9oZrDhO9BOYt/giphy.gif",
                  "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHE0OTVkMjNhajJkOWhvMG5ldWVycWk3dXZ0NXZtbzhhYzV2YTc2YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/H7kfFDvD9HSYGRbvid/giphy.gif",
                  "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3Jlb2NmODh2cnl6MTI5N2w5Zmo5aDBsaXhncW5idm5iMjE5MnczYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zhRA0okWxTGiu78uSk/giphy.gif"]
        async with httpx.AsyncClient() as client:    
            await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "channel": user,  # or any valid channel/user ID
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "🧘 *Take a moment to breathe.*\nInhale slowly... hold... and exhale.\nYou got this 🌱"
                        }
                    },
                    {
                        "type": "image",
                        "image_url": random.choice(images),
                        "alt_text": "Calming breathing animation"
                    }
                ]
            }
            )
            async with httpx.AsyncClient() as client:
                response = await client.post(
                "https://slack.com/api/dnd.setSnooze",
                headers={
                    "Authorization": f"Bearer {SLACK_USER_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "num_minutes": 10
                }
            )
        data = response.json()
        if not data.get("ok"):
            print("Failed to set DND:", data)
        else:
            print(f"✅ DND set for 10 minutes.")
    if form.get("command") == "/hello":
        async with httpx.AsyncClient() as client:
            await client.post(
                SLACK_API_URL,
                headers={
                    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "channel": "C08NKQ37J5N",
                    "text": f"👋 Hey!"
                }
            )

    return {
            "response_type": "ephemeral",
            "text": "Slash command processed!"
        }