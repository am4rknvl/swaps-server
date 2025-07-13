from fastapi import WebSocket, APIRouter

router = APIRouter()

clients = {}  # session_id: websocket

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    clients[session_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        del clients[session_id]

# Utility function to push notif
async def push_notification(session_id: str, message: str):
    if session_id in clients:
        await clients[session_id].send_text(message)
