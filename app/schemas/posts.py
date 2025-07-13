from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    text: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    voice_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None
    hashtags: Optional[List[str]] = None
    is_anonymous: bool = False

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime
    user_id: Optional[int]

    class Config:
        orm_mode = True
