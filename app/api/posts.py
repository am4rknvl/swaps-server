from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import re

from app.schemas.posts import PostCreate, PostOut
from app.models.post import Post
from app.models.hashtag import Hashtag
from app.models.post_hashtag import PostHashtag
from app.database import get_db

router = APIRouter()

def extract_hashtags(text: str):
    return re.findall(r"#(\w+)", text or "")

@router.post("/", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(
        text=post.text,
        image_url=post.image_url,
        voice_url=post.voice_url,
        video_url=post.video_url,
        is_anonymous=post.is_anonymous,
        user_id=None  # TODO: Update when auth added
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Extract and attach hashtags
    tags = extract_hashtags(post.text)
    for tag_text in tags:
        tag_text = tag_text.lower()
        tag = db.query(Hashtag).filter_by(tag=tag_text).first()
        if not tag:
            tag = Hashtag(tag=tag_text)
            db.add(tag)
            db.commit()
            db.refresh(tag)

        link = PostHashtag(post_id=db_post.id, hashtag_id=tag.id)
        db.add(link)

    db.commit()  # Commit all tag links together
    return db_post


@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).all()


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
