from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Base
from app.models.social import Follow, User
from typing import List
from app.api.auth import get_current_user   # assuming JWT or Clerk integration

router = APIRouter(prefix="/social", tags=["Social"])

@router.post("/follow/{user_id}", status_code=201)
def follow_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You can't follow yourself.")
 
    existing = db.query(Follow).filter_by(follower_id=current_user.id, following_id=user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already following.")

    follow = Follow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    db.commit()
    return {"msg": "Followed successfully"}

@router.delete("/unfollow/{user_id}")
def unfollow_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow = db.query(Follow).filter_by(follower_id=current_user.id, following_id=user_id).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Not following")

    db.delete(follow)
    db.commit()
    return {"msg": "Unfollowed successfully"}

@router.get("/followers/{user_id}", response_model=List[int])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(Follow).filter_by(following_id=user_id).all()
    return [f.follower_id for f in followers]

@router.get("/following/{user_id}", response_model=List[int])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = db.query(Follow).filter_by(follower_id=user_id).all()
    return [f.following_id for f in following]
