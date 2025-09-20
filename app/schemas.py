from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

# ========== User Schemas ==========
class UserCreate(BaseModel):
    name: str
    dob: date
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    dob: date
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ========== Creator Schemas ==========
class CreatorCreate(BaseModel):
    platform: str
    platform_id: str

class CreatorResponse(BaseModel):
    id: UUID
    platform: str
    platform_id: str
    class Config:
        from_attributes = True

# ========== Flag Schemas ==========
class FlagCreate(BaseModel):
    creator_id: UUID

class FlagResponse(BaseModel):
    id: UUID
    creator_id: UUID
    flagged_by: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ========== Gemini Prompt Schemas ==========
class GeminiRequest(BaseModel):
    prompt: str = Field(..., example="Explain quantum computing in simple terms")

class GeminiResponse(BaseModel):
    result: str

# ========== Misinformation Check Schemas ==========
class MisinformationCheckRequest(BaseModel):
    content: Optional[str] = Field(None, example="Webpage text to check for misinformation")
    url: Optional[str] = Field(None, example="https://www.youtube.com/watch?v=abc123")
    platform: Optional[str] = Field(None, example="youtube")

class MisinformationCheckResponse(BaseModel):
    is_misinformation: bool

# ========== Gemini Citations Schemas ==========
class GeminiCitationsRequest(BaseModel):
    content: Optional[str] = Field(None, example="Webpage text to analyze")
    url: Optional[str] = Field(None, example="https://www.example.com")
    platform: Optional[str] = Field(None, example="reddit")

class Citation(BaseModel):
    title: str
    url: str
    summary: Optional[str] = None

class GeminiCitationsResponse(BaseModel):
    supporting_sources: List[Citation]
    opposing_sources: List[Citation]