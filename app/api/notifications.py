from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.notification import Notification
from app.schemas.notifications import NotificationOut

router = APIRouter()

@router.get("/", response_model=List[NotificationOut])
def get_notifications(session_id: str, db: Session = Depends(get_db)):
    notifs = (
        db.query(Notification)
        .filter(Notification.session_id == session_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return notifs

@router.post("/{id}/mark-read")
def mark_notification_read(id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    return {"status": "ok"}
