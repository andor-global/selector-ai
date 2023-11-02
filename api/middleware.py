import os
from fastapi import Request, HTTPException
from jwt import PyJWTError, decode as jwt_decode
from pydantic import ValidationError


async def auth_middleware(request: Request, call_next):
    try:
        token = request.cookies.auth_token
        decoded_token = jwt_decode(
            token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        request.state.user = decoded_token
        response = await call_next(request)
        return response
    except (PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Token validation failed")


async def validate_image():
    pass
