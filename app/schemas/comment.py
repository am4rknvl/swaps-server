from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: int
    parent_id: Optional[int] = None
    text: str
    session_id: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    parent_id: Optional[int]
    text: str
    session_id: str
    created_at: datetime
    replies: List['CommentOut'] = []

    class Config:
        orm_mode = True

CommentOut.update_forward_refs()
