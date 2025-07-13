from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentOut
from typing import List

router = APIRouter()

@router.post("/", response_model=CommentOut)
def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/post/{post_id}", response_model=List[CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id, Comment.parent_id == None).all()

    def build_thread(c):
        return CommentOut(
            id=c.id,
            post_id=c.post_id,
            parent_id=c.parent_id,
            text=c.text,
            session_id=c.session_id,
            created_at=c.created_at,
            replies=[build_thread(r) for r in c.replies]
        )

    return [build_thread(c) for c in comments]
