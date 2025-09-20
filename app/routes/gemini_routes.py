
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import GeminiRequest, GeminiResponse, MisinformationCheckRequest, MisinformationCheckResponse, GeminiCitationsRequest, GeminiCitationsResponse
from ..gemini_proxy import call_gemini
import httpx

router = APIRouter(prefix="/gemini", tags=["Gemini"])

# Endpoint for citations/sources for and against content
@router.post("/get_citations", response_model=GeminiCitationsResponse)
async def get_citations(request: GeminiCitationsRequest):
    try:
        # Auto-detect platform from URL if not provided
        platform = request.platform
        if not platform and request.url:
            url = request.url.lower()
            if "youtube.com" in url:
                platform = "youtube"
            elif "reddit.com" in url:
                platform = "reddit"
            elif "instagram.com" in url or "insta" in url:
                platform = "insta"
            elif "x.com" in url or "twitter.com" in url:
                platform = "x"
            else:
                platform = "unknown"

        # Fetch content from URL if not provided
        content = request.content
        if not content and request.url:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(request.url)
                    resp.raise_for_status()
                    content = resp.text
            except Exception:
                raise HTTPException(status_code=400, detail="Could not fetch content from URL")

        if not content:
            raise HTTPException(status_code=400, detail="No content provided or found")

        # Compose prompt for Gemini
        prompt = (
            f"For the following content from {platform}, generate two lists: "
            f"1. Sources/articles/citations supporting the content. "
            f"2. Sources/articles/citations opposing the content. "
            f"Return each list as JSON with title, url, and summary. Content: {content}"
        )
        result = await call_gemini(prompt)

        # Try to parse Gemini's response as JSON
        import json
        try:
            parsed = json.loads(result)
            supporting = parsed.get("supporting_sources", [])
            opposing = parsed.get("opposing_sources", [])
        except Exception:
            # Fallback: empty lists if parsing fails
            supporting = []
            opposing = []

        return GeminiCitationsResponse(supporting_sources=supporting, opposing_sources=opposing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", response_model=GeminiResponse)
async def ask_gemini(request: GeminiRequest):
    try:
        result = await call_gemini(request.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint for misinformation check
@router.post("/check_misinformation", response_model=MisinformationCheckResponse)
async def check_misinformation(request: MisinformationCheckRequest):
    try:
        # Auto-detect platform from URL if not provided
        platform = request.platform
        if not platform and request.url:
            url = request.url.lower()
            if "youtube.com" in url:
                platform = "youtube"
            elif "reddit.com" in url:
                platform = "reddit"
            elif "instagram.com" in url or "insta" in url:
                platform = "insta"
            elif "x.com" in url or "twitter.com" in url:
                platform = "x"
            else:
                platform = "unknown"

        # Fetch content from URL if not provided
        content = request.content
        if not content and request.url:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(request.url)
                    resp.raise_for_status()
                    # Simple extraction: get text content
                    content = resp.text
            except Exception:
                raise HTTPException(status_code=400, detail="Could not fetch content from URL")

        if not content:
            raise HTTPException(status_code=400, detail="No content provided or found")

        # Compose prompt for Gemini
        prompt = f"Check if the following content from {platform} contains misinformation. Reply only true or false. Content: {content}"
        result = await call_gemini(prompt)
        # Normalize Gemini response
        is_misinfo = str(result).strip().lower() == "true"
        return {"is_misinformation": is_misinfo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))