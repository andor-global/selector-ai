import asyncio
import base64
from datetime import datetime
import io
import os
from pathlib import Path
import uuid
from PIL import Image
from fastapi import APIRouter, Depends, WebSocket
import requests
from websockets.exceptions import ConnectionClosed
from chat.chat import Chat

from ..models.user import User
from ..models.generation import Generation
from ..middleware import validate_websocket_auth

router = APIRouter()


@router.websocket("/chat")
async def endpoint(websocket: WebSocket, user_id: str = Depends(validate_websocket_auth)):
    await websocket.accept()
    try:
        user = await User.get(user_id)

        user_profile_info = {
            "gender": user.sex,
            "age": user.get_age(),
            "personality_description": user.get_psychotype_info()["description"],
        }

        chat = Chat(memory_state={}, user_profile_info=user_profile_info)

        while True:
            user_input = await websocket.receive_text()
            chat_output = chat.execute(user_input)

            await websocket.send_json({"type": "chat", "message": chat_output['style_look_description']})

            await websocket.send_json({"type": "image", "name": chat_output['image_url']})

            asyncio.create_task(save_image(user, chat_output['image_url']))
    except ConnectionClosed:
        print("connection is closed")
        return ""


async def save_image(user: User, image_url: str):
    image_bytes = requests.get(image_url).content

    image = Image.open(io.BytesIO(image_bytes))

    relative_path = Path.cwd() / "static"
    unique_name = f"{uuid.uuid4()}-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.jpg"
    output_path = relative_path / unique_name

    image.save(output_path)

    encoded_image = base64.b64encode(io.BytesIO(image_bytes).read()).decode('utf-8')
    generation = Generation(
        user=user,
        prompt=[""],
        name=unique_name,
        image=encoded_image
    )

    await generation.save()
