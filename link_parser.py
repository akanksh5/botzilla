import os
import httpx
from dotenv import load_dotenv
import json
load_dotenv()
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def process_link(url: str):
    prompt = f"""
    Categorize and tag this URL: {url}
    Respond in JSON like:
    {{
      "title": "Page Title",
      "category": "Blog",
      "tags": ["AI", "Slack", "Bots"]
    }}
    """

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
            }
        )
        content = res.json()["choices"][0]["message"]["content"]
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
    try:
        data = json.loads(cleaned)
        return data["title"], data["category"], data["tags"]
    except json.JSONDecodeError:
        print("Failed to parse GPT response:", cleaned)
        return "Unknown Title", "Uncategorized", []