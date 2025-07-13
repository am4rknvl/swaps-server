from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hashtag import Hashtag
from app.models.post import Post
from app.models.post_hashtag import PostHashtag
from app.schemas.posts import PostOut
from datetime import datetime
from app.utils.reactions import get_reaction_counts
from typing import List
import math

router = APIRouter()

@router.get("/fresh", response_model=List[PostOut])
def get_fresh_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).limit(50).all()


@router.get("/trending", response_model=List[PostOut])
def get_trending_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    now = datetime.utcnow()

    scored_posts = []

    for post in posts:
        reactions = get_reaction_counts(db, post.id)
        hours = (now - post.created_at).total_seconds() / 3600
        hours = max(hours, 1)  # prevent divide by zero

        score = (
            reactions["laugh"] * 3 +
            reactions["skull"] * 2 +
            reactions["cry"] * 1
        ) / math.pow((hours + 2), 1.2)

        scored_posts.append((score, post))

    # sort descending by score
    sorted_posts = sorted(scored_posts, key=lambda x: x[0], reverse=True)
    return [p for _, p in sorted_posts[:50]]

@router.get("/tag/{tag}", response_model=List[PostOut])
def get_posts_by_tag(tag: str, db: Session = Depends(get_db)):
    tag = db.query(Hashtag).filter_by(tag=tag.lower()).first()
    if not tag:
        return []

    post_links = db.query(PostHashtag).filter_by(hashtag_id=tag.id).all()
    post_ids = [pl.post_id for pl in post_links]

    posts = db.query(Post).filter(Post.id.in_(post_ids)).order_by(Post.created_at.desc()).limit(50).all()
    return posts
