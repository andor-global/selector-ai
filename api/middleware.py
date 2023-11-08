import base64
import os
from jwt import PyJWTError, decode as jwt_decode
from fastapi import Depends, Request, HTTPException
from pydantic import ValidationError


async def verify_auth(request: Request):
    try:
        token = request.cookies["auth_token"]
        decoded_token = jwt_decode(
            token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        request.state.user_id = decoded_token["user_id"]
    except (PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Token validation failed")


async def validate_image(img: str):
    if img is not None and img.startswith("data:image/"):
        data, encoded_data = img.split(",", 1)
        decoded_data = base64.b64decode(encoded_data)

        max_image_size = 1024
        if len(decoded_data) > max_image_size:
            raise HTTPException(
                status_code=400, detail="Image size exceeds the limit")
    return img
