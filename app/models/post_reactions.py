from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class PostReaction(Base):
    __tablename__ = "post_reactions"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    reaction_type = Column(String)  # 'laugh', 'cry', 'skull'
    session_id = Column(String, index=True)  # to support anon users

    __table_args__ = (UniqueConstraint("post_id", "session_id", name="unique_post_reaction"),)

    post = relationship("Post", back_populates="reactions")
