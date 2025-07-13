from sqlalchemy.orm import Session
from app.models.post_reactions import PostReaction

def get_reaction_counts(db: Session, post_id: int):
    counts = {"laugh": 0, "cry": 0, "skull": 0}
    reactions = db.query(PostReaction).filter_by(post_id=post_id).all()
    for r in reactions:
        counts[r.reaction_type] += 1
    return counts
