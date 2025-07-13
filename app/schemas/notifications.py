from pydantic import BaseModel
from datetime import datetime

class NotificationOut(BaseModel):
    id: int
    session_id: str
    type: str
    post_id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True
