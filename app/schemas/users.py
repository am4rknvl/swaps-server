from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    location: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    referral_code: Optional[str] = None

class UserRead(UserBase):
    id: int
    credibility_score: Optional[float] = 0.0
    rating: Optional[float] = 0.0
    referral_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    credibility_score: Optional[float] = 0.0
    rating: Optional[float] = 0.0
    referral_code: Optional[str] = None

    class Config:
        orm_mode = True