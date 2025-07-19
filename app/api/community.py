from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Community, CommunityMember, User
from schemas import CommunityCreate, CommunityOut
from auth import get_current_user
from database import get_db
from typing import List

router = APIRouter(prefix="/communities", tags=["Communities"])

@router.post("/", response_model=CommunityOut)
def create_community(data: CommunityCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if db.query(Community).filter((Community.name == data.name) | (Community.slug == data.slug)).first():
        raise HTTPException(status_code=400, detail="Community name or slug already exists")
    
    new_community = Community(
        name=data.name,
        slug=data.slug,
        description=data.description,
        creator_id=user.id
    )
    db.add(new_community)
    db.commit()
    db.refresh(new_community)

    # Auto-join creator
    db.add(CommunityMember(community_id=new_community.id, user_id=user.id))
    db.commit()
    
    return new_community

@router.get("/", response_model=List[CommunityOut])
def list_communities(db: Session = Depends(get_db)):
    return db.query(Community).order_by(Community.created_at.desc()).all()

@router.get("/{slug}", response_model=CommunityOut)
def get_community(slug: str, db: Session = Depends(get_db)):
    community = db.query(Community).filter_by(slug=slug).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community

@router.post("/{slug}/join")
def join_community(slug: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    community = db.query(Community).filter_by(slug=slug).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    existing = db.query(CommunityMember).filter_by(community_id=community.id, user_id=user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already a member")

    db.add(CommunityMember(community_id=community.id, user_id=user.id))
    db.commit()
    return {"msg": f"Joined {slug}"}

@router.delete("/{slug}/leave")
def leave_community(slug: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    community = db.query(Community).filter_by(slug=slug).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    membership = db.query(CommunityMember).filter_by(community_id=community.id, user_id=user.id).first()
    if not membership:
        raise HTTPException(status_code=400, detail="Not a member")

    db.delete(membership)
    db.commit()
    return {"msg": f"Left {slug}"}

@router.get("/{slug}/members", response_model=List[int])
def list_members(slug: str, db: Session = Depends(get_db)):
    community = db.query(Community).filter_by(slug=slug).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    members = db.query(CommunityMember).filter_by(community_id=community.id).all()
    return [m.user_id for m in members]
