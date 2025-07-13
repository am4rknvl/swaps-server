from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.profile import Profile
from app.api.auth import get_current_user

from app.schemas.profiles import ProfileCreate, ProfileRead

router = APIRouter()

@router.post("/profiles", response_model=ProfileRead)
async def create_profile(
    payload: ProfileCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    existing_profile = result.scalar_one_or_none()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = Profile(user_id=user_id, **payload.dict())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile
