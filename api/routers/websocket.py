import asyncio
from datetime import datetime
import io
import os
from pathlib import Path
import uuid
from PIL import Image
from fastapi import APIRouter, Depends, WebSocket
import requests
from websockets.exceptions import ConnectionClosed
from chat.chain import create_chain

from chat.memory import create_memory
from ..models.user import User
from ..middleware import validate_websocket_auth

router = APIRouter()


@router.websocket("/chat")
async def endpoint(websocket: WebSocket, user_id: str = Depends(validate_websocket_auth)):
    await websocket.accept()
    try:
        user = await User.get(user_id)

        memory = create_memory(memory_state={})
        chain = create_chain(memory)

        chain_input = {
            "gender": user.sex,
            "age": user.get_age(),
            "psychotype_description": user.get_psychotype_info()["description"],
        }

        while True:
            user_input = await websocket.receive_text()
            chain_output["text"] = user_input

            chain_output = chain.invoke(chain_input)

            style_look_description = chain_output["style look description"]
            image_url = chain_output["image"]

            websocket.send_json({"type": "chat", "message": style_look_description})

            memory.save_context({"input": user_input}, {"output": style_look_description})

            websocket.send_json({"type": "image", "name": image_url})

            asyncio.create_task(save_image(image_url))
    except ConnectionClosed:
        print("connection is closed")
        return ""


async def save_image(image_url: str):
    image_bytes = requests.get(image_url).content

    image = Image.open(io.BytesIO(image_bytes))

    relative_path = os.path.join("..", "..", "static")
    unique_name = f"{uuid.uuid4()}-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.jpg"
    output_path = os.path.join(relative_path, unique_name)

    relative_path = Path("../../static")
    unique_name = f"{uuid.uuid4()}-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.jpg"
    output_path = relative_path / unique_name

    image.save(output_path)

    # TODO: add to database what type of prompt generated this image
