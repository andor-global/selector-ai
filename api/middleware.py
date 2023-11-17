import os
from jwt import PyJWTError, decode as jwt_decode
from fastapi import Query, Request, HTTPException, WebSocketException
from pydantic import ValidationError


async def validate_websocket_auth(auth_token: str = Query(...)) -> str:
    try:
        decoded_token = jwt_decode(auth_token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return decoded_token["user_id"]
    except (PyJWTError, ValidationError, KeyError):
        raise WebSocketException(status_code=403, detail="Auth token validation failed")


async def validate_http_auth(request: Request):
    try:
        token = request.cookies["auth_token"]
        decoded_token = jwt_decode(
            token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        request.state.user_id = decoded_token["user_id"]
    except (PyJWTError, ValidationError, KeyError):
        raise HTTPException(status_code=403, detail="Auth token validation failed")
