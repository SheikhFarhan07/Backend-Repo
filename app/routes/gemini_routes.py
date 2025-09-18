from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import GeminiRequest, GeminiResponse
from ..gemini_proxy import call_gemini

router = APIRouter(prefix="/gemini", tags=["Gemini"])

@router.post("/ask", response_model=GeminiResponse)
async def ask_gemini(request: GeminiRequest):
    try:
        result = await call_gemini(request.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))