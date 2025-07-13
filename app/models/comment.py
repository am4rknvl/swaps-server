from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    text = Column(Text, nullable=False)
    session_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    replies = relationship("Comment", backref="parent", cascade="all, delete")
