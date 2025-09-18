from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import date, datetime
from enum import Enum
from typing import Optional

# ----- Platform Enum -----
class PlatformEnum(str, Enum):
    youtube = "youtube"
    x = "x"
    reddit = "reddit"
    insta = "insta"

# ----- User Schemas -----
class UserCreate(BaseModel):
    name: str
    dob: date
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: UUID
    name: str
    dob: date
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----- Creator Schemas -----
class CreatorCreate(BaseModel):
    platform: PlatformEnum
    platform_id: str

class CreatorResponse(BaseModel):
    id: UUID
    platform: PlatformEnum
    platform_id: str
    class Config:
        from_attributes = True

# ----- Flag Schemas -----
class FlagCreate(BaseModel):
    creator_id: UUID

class FlagResponse(BaseModel):
    id: UUID
    creator_id: UUID
    flagged_by: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ----- Gemini Schemas -----
class GeminiRequest(BaseModel):
    prompt: str = Field(..., example="Explain quantum computing in simple terms")

class GeminiResponse(BaseModel):
    result: str