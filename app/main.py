from fastapi import FastAPI
from app.api.auth import auth_router
from app.api.posts import router as posts_router
from app.api.reaction import router as reactions_router
from app.api.comment import router as comments_router
from app.api.profiles import router as profiles_router 
from app.api.feed import router as feed_router



app = FastAPI(title="Swaps API", version="1.0")

# Route registration
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
app.include_router(reactions_router, prefix="/reactions", tags=["reactions"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(feed_router, prefix="/feed", tags=["feed"])
from app.api.notifications import router as notifications_router
app.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
from app.ws.notifications import router as ws_notifications_router

app.include_router(ws_notifications_router, prefix="/ws", tags=["websocket"])
