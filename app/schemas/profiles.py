from pydantic import BaseModel
from typing import Optional, List

class ProfileCreate(BaseModel):
    display_name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = []

class ProfileUpdate(BaseModel):
    display_name: Optional[str]
    bio: Optional[str]
    location: Optional[str]


class ProfileRead(ProfileCreate):
    id: str
    user_id: str

    class Config:
        orm_mode = True
