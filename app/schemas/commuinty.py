from pydantic import BaseModel
from datetime import datetime

class CommunityBase(BaseModel):
    name: str
    slug: str
    description: str = ""

class CommunityCreate(CommunityBase):
    pass

class CommunityOut(CommunityBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True
