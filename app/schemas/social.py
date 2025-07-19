from pydantic import BaseModel

class FollowBase(BaseModel):
    follower_id: int
    following_id: int

class FollowOut(BaseModel):
    follower_id: int
    following_id: int

    class Config:
        orm_mode = True
