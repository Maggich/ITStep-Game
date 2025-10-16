from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    db: str
    version: Optional[str] = None