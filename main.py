from fastapi import FastAPI, Request, Response
import os
from dotenv import load_dotenv
import httpx
import random
from fastapi.responses import JSONResponse
import json
import sqlite3
from datetime import datetime
from link_parser import process_link
from models import save_link_data, get_latest_links, get_links_by_tag

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

@app.post("/slack/retro")
async def retro_command(request: Request):
    form = await request.form()
    trigger_id = form.get("trigger_id")

    async with httpx.AsyncClient() as client:
        await client.post(
            "https://slack.com/api/views.open",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            json={
                "trigger_id": trigger_id,
                "view": {
                    "type": "modal",
                    "callback_id": "retro_feedback",
                    "title": {"type": "plain_text", "text": "RetroBot"},
                    "submit": {"type": "plain_text", "text": "Submit"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "went_well",
                            "label": {"type": "plain_text", "text": "✅ What went well?"},
                            "element": {
                                "type": "plain_text_input",
                                "multiline": True,
                                "action_id": "answer"
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "went_wrong",
                            "label": {"type": "plain_text", "text": "❌ What didn’t go well?"},
                            "element": {
                                "type": "plain_text_input",
                                "multiline": True,
                                "action_id": "answer"
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "improvements",
                            "label": {"type": "plain_text", "text": "💡 What can be improved?"},
                            "element": {
                                "type": "plain_text_input",
                                "multiline": True,
                                "action_id": "answer"
                            }
                        }
                    ]
                }
            }
        )
    return {"response_type": "ephemeral", "text": "Launching Retro Modal..."}

@app.post("/slack/interactions")
async def slack_interactions(request: Request):
    payload = await request.form()
    data = json.loads(payload.get("payload"))

    if data["type"] == "view_submission" and data["view"]["callback_id"] == "retro_feedback":
        user_id = data["user"]["id"]
        state = data["view"]["state"]["values"]

        # Extract answers
        went_well = state["went_well"]["answer"]["value"]
        went_wrong = state["went_wrong"]["answer"]["value"]
        improvements = state["improvements"]["answer"]["value"]

        # Save to SQLite
        conn = sqlite3.connect("retro.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                went_well TEXT,
                went_wrong TEXT,
                improvements TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO feedback (user_id, went_well, went_wrong, improvements)
            VALUES (?, ?, ?, ?)
        """, (user_id, went_well, went_wrong, improvements))
        conn.commit()
        conn.close()

        return JSONResponse(content={"response_action": "clear"})  # Dismiss modal
    
    if data["type"] == "view_submission" and data["view"]["callback_id"] == "vibecheck_modal":
        user_id = data["user"]["id"]
        username = data["user"].get("username", "anonymous")
        vibe = data["view"]["state"]["values"]["vibe"]["answer"]["value"]
        submitted_at = datetime.now().isoformat()

        conn = sqlite3.connect("vibe.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vibes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                username TEXT,
                vibe TEXT,
                submitted_at TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO vibes (user_id, username, vibe, submitted_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, vibe, submitted_at))
        conn.commit()
        conn.close()

        if any(word in vibe.lower() for word in ["sad", "down", "tired", "depressed","low"]):
            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://slack.com/api/chat.postMessage",
                    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
                    json={
                        "channel": user_id,
                        "text": (
                            "Hey there 💕 it looks like you're having a tough day.\n"
                            "Here are a few things that might help:\n\n"
                            "🌿 Take a short walk in nature\n"
                            "🎵 Try a 5-minute meditation: <https://www.youtube.com/watch?v=inpok4MKVLM>\n"
                            "🙏 And remember, it's okay to feel this way. You're not alone."
                        )
                    }
                )

        return JSONResponse(content={"response_action": "clear"})
    
    if data["type"] == "view_submission" and data["view"]["callback_id"] == "standup_submission":
        user_id = data["user"]["id"]
        username = data["user"]["username"]
        state = data["view"]["state"]["values"]

        yesterday = state["yesterday"]["answer"]["value"]
        today = state["today"]["answer"]["value"]
        blockers = state["blockers"]["answer"]["value"]

        submitted_at = datetime.now().isoformat()

        conn = sqlite3.connect("standup.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS standup (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                username TEXT,
                yesterday TEXT,
                today TEXT,
                blockers TEXT,
                submitted_at TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO standup (user_id, username, yesterday, today, blockers, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, yesterday, today, blockers, submitted_at))
        conn.commit()
        conn.close()

        return JSONResponse(content={"response_action": "clear"})

@app.post("/slack/summary")
async def retro_summary(request: Request):
    form = await request.form()
    channel_id = form.get("channel_id")

    # Fetch retro data
    conn = sqlite3.connect("retro.db")
    cursor = conn.cursor()
    cursor.execute("SELECT went_well, went_wrong, improvements FROM feedback")
    rows = cursor.fetchall()
    conn.close()

    # Create anonymized summary
    if not rows:
        return {"response_type": "ephemeral", "text": "No retro feedback found."}

    def bullet_list(items):
        return "\n".join([f"• {item.strip()}" for item in items if item.strip()])

    well = bullet_list([row[0] for row in rows])
    wrong = bullet_list([row[1] for row in rows])
    improve = bullet_list([row[2] for row in rows])

    summary = f"""🚀 *Sprint Retro Summary*

✅ *What went well:*
{well or '—'}

❌ *What didn’t go well:*
{wrong or '—'}

💡 *Suggestions for improvement:*
{improve or '—'}
"""

    # Optional: Post to channel via chat.postMessage
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "channel": channel_id,
                "text": summary
            }
        )

    return {"response_type": "ephemeral", "text": "🧾 Retro summary posted to channel!"}


@app.post("/slack/standup")
async def open_standup_modal(request: Request):
    form = await request.form()
    trigger_id = form.get("trigger_id")
    user_id = form.get("user_id")

    view = {
        "type": "modal",
        "callback_id": "standup_submission",
        "title": {"type": "plain_text", "text": "Daily Standup"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "blocks": [
            {
                "type": "input",
                "block_id": "yesterday",
                "label": {"type": "plain_text", "text": "🕙 What did you do yesterday?"},
                "element": {"type": "plain_text_input", "action_id": "answer", "multiline": True}
            },
            {
                "type": "input",
                "block_id": "today",
                "label": {"type": "plain_text", "text": "📅 What will you do today?"},
                "element": {"type": "plain_text_input", "action_id": "answer", "multiline": True}
            },
            {
                "type": "input",
                "block_id": "blockers",
                "label": {"type": "plain_text", "text": "🚧 Any blockers?"},
                "element": {"type": "plain_text_input", "action_id": "answer", "multiline": True}
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            "https://slack.com/api/views.open",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            json={"trigger_id": trigger_id, "view": view}
        )

    return {"response_type": "ephemeral", "text": "Opening standup modal..."}

@app.post("/slack/standup-summary")
async def standup_summary(request: Request):
    form = await request.form()
    channel_id = form.get("channel_id")

    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("standup.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, yesterday, today, blockers
        FROM standup
        WHERE DATE(submitted_at) = ?
    """, (today,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"response_type": "ephemeral", "text": "No standup updates submitted today."}

    summary = "*🚀 Daily Standup Summary:*\n\n"
    for username, yday, tday, block in rows:
        summary += f"*👤 {username}*\n"
        summary += f"> *Yesterday:* {yday.strip()}\n"
        summary += f"> *Today:* {tday.strip()}\n"
        summary += f"> *Blockers:* {block.strip() or 'None'}\n\n"

    # Post to channel
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            json={"channel": channel_id, "text": summary}
        )

    return {"response_type": "ephemeral", "text": "✅ Standup summary posted!"}

# Vibe Check Slash Command
@app.post("/slack/vibecheck")
async def vibecheck_command(request: Request):
    form = await request.form()
    trigger_id = form.get("trigger_id")

    view = {
        "type": "modal",
        "callback_id": "vibecheck_modal",
        "title": {"type": "plain_text", "text": "Vibe Check"},
        "submit": {"type": "plain_text", "text": "Share"},
        "blocks": [
            {
                "type": "input",
                "block_id": "vibe",
                "label": {"type": "plain_text", "text": "How are you feeling today?"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "answer",
                    "multiline": True,
                    "placeholder": {"type": "plain_text", "text": "e.g. 🛌 Sleepy but ready!"}
                }
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            "https://slack.com/api/views.open",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            json={"trigger_id": trigger_id, "view": view}
        )

    return {"response_type": "ephemeral", "text": "Vibe check modal launched!"}

@app.post("/slack/vibesummary")
async def vibe_summary(request: Request):
    form = await request.form()
    channel_id = form.get("channel_id")

    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("vibe.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vibe FROM vibes
        WHERE DATE(submitted_at) = ?
    """, (today,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"response_type": "ephemeral", "text": "No vibes shared today!"}

    summary =  f"*🚀 Vibe Check Summary ({today})*\n\n"
    for i, (vibe,) in enumerate(rows, start=1):
        summary += f"*Entry {i}*: {vibe.strip()}\n"

    async with httpx.AsyncClient() as client:
        await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            json={"channel": channel_id, "text": summary}
        )

    return Response(status_code=200)

@app.post("/slack/linklibrarian")
async def handle_slash_command(request: Request):
    form = await request.form()
    text = form.get("text", "").strip()
    user_id = form.get("user_id")

    args = text.split()
    if not args:
        return JSONResponse({"text": "Usage: add <url> | latest | tag <tag>"})

    command = args[0].lower()

    if command == "add" and len(args) > 1:
        url = args[1]
        title, category, tags = await process_link(url)
        save_link_data(url, title, category, tags)
        return JSONResponse({"text": f"✅ Added <{url}|{title}> as *{category}* with tags: `{', '.join(tags)}`"})

    elif command == "latest":
        links = get_latest_links()
        if not links:
            return JSONResponse({"text": "No links found!"})
        text = "\n".join([f"<{l['url']}|{l['title']}> ({l['category']}) [{l['tags']}]" for l in links])
        return JSONResponse({"text": f"*Latest Links:*\n{text}"})

    elif command == "tag" and len(args) > 1:
        tag = args[1]
        links = get_links_by_tag(tag)
        if not links:
            return JSONResponse({"text": f"No links found with tag `{tag}`"})
        text = "\n".join([f"<{l['url']}|{l['title']}> ({l['category']}) [{l['tags']}]" for l in links])
        return JSONResponse({"text": f"*Links tagged `{tag}`:*\n{text}"})

    return JSONResponse({"text": "Invalid command. Try: `add <url>`, `latest`, or `tag <tag>`"})