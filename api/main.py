import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers.auth import router as auth_router
from .routers.chat import router as chat_router
from .routers.user import router as user_router
from .routers.websocket import router as ws_router
from .db import lifespan

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_DEPLOYMENT"), "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(chat_router, prefix="/api/chat")
app.include_router(user_router, prefix="/api/user")

app.include_router(ws_router, prefix="/ws")


@app.get("/")
def read_root():
    return {"message": "Welcome to GenL API"}
