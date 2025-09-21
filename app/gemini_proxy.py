import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def call_gemini(prompt: str) -> str:
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
            # Defensive: return the whole response if expected keys are missing
        try:
            candidates = data.get("candidates", [{}])
            if not candidates or not isinstance(candidates, list):
                return str(data)
            content = candidates[0].get("content", {})
            parts = content.get("parts", [{}])
            if not parts or not isinstance(parts, list):
                return str(data)
            text = parts[0].get("text", None)
            if text is None:
                return str(data)
            return text
        except Exception:
            return str(data)