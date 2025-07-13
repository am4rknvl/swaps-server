from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, index=True)

    posts = relationship("PostHashtag", back_populates="hashtag", cascade="all, delete")
