import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def call_gemini(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")