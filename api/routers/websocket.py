import asyncio
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from ..models.user import User
from ..middleware import validate_websocket_auth

router = APIRouter()


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Depends(validate_websocket_auth)):
    await websocket.accept()
    try:
        user = await User.find_one({'_id': user_id})
        send_images_task = asyncio.create_task(send_generated_images(websocket))

        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except ConnectionClosed:
        return ""


async def websocket_receiver(websocket: WebSocket):
    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            # Process the received message (you can handle it according to your needs)
    except WebSocketDisconnect:
        pass


async def send_generated_images(websocket: WebSocket):
    await asyncio.sleep(5)
    await asyncio.gather(websocket.send_text("generated an image"))
