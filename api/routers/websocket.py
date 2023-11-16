from fastapi import APIRouter, Depends, WebSocket
from websockets.exceptions import ConnectionClosed
from middleware import validate_websocket_auth

router = APIRouter()


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, user_info: dict = Depends(validate_websocket_auth)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except ConnectionClosed:
        return ""
