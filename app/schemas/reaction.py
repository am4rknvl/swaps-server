from pydantic import BaseModel
from typing import Literal

class ReactionCreate(BaseModel):
    reaction_type: Literal["laugh", "cry", "skull"]
    session_id: str  # generated client-side

class ReactionOut(BaseModel):
    post_id: int
    laugh: int
    cry: int
    skull: int
