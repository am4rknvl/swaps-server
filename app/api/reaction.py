from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.post_reactions import PostReaction
from app.models.post import Post
from app.models.notification import Notification  # ✅ Import it
from app.schemas.reaction import ReactionCreate, ReactionOut
import asyncio
from app.ws.notifications import push_notification


router = APIRouter()

@router.post("/react", response_model=ReactionOut)
def react_to_post(reaction: ReactionCreate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == reaction.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = db.query(PostReaction).filter_by(
        post_id=reaction.post_id, session_id=reaction.session_id
    ).first()

    if existing:
        existing.reaction_type = reaction.reaction_type
    else:
        new_reaction = PostReaction(
            post_id=reaction.post_id,
            session_id=reaction.session_id,
            reaction_type=reaction.reaction_type
        )
        db.add(new_reaction)

    # 🔔 Trigger notification if post owner has session_id
    if post.session_id and post.session_id != reaction.session_id:  # avoid self-notif
        notif = Notification(
            session_id=post.session_id,
            type="reaction",
            post_id=post.id,
            message=f"Someone reacted to your post with {reaction.reaction_type}"
        )
        db.add(notif)

        

    db.commit()

    # ✅ Count reactions
    counts = {"laugh": 0, "cry": 0, "skull": 0}
    all_reactions = db.query(PostReaction).filter_by(post_id=reaction.post_id).all()
    for r in all_reactions:
        counts[r.reaction_type] += 1

    return {
        "post_id": reaction.post_id,
        **counts
    }

@router.get("/{post_id}", response_model=ReactionOut)
def get_reactions(post_id: int, db: Session = Depends(get_db)):
    reactions = db.query(PostReaction).filter_by(post_id=post_id).all()

    counts = {"laugh": 0, "cry": 0, "skull": 0}
    for r in reactions:
        counts[r.reaction_type] += 1

    return {
        "post_id": post_id,
        **counts
    }
