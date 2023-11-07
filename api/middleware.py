import base64
import os
from fastapi import Depends, Request, HTTPException
from jwt import PyJWTError, decode as jwt_decode
from pydantic import ValidationError


async def verify_auth(request: Request, call_next):
    try:
        token = request.cookies.auth_token
        decoded_token = jwt_decode(
            token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        request.state.user = decoded_token
        response = await call_next(request)
        return response
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
