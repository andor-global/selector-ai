import os
import asyncio
from mongoengine import connect
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers.auth import router as auth_router
from .routers.model import router as model_router
from .routers.chat import router as chat_router
from .routers.user import router as user_router

dotenv_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../.env"))
load_dotenv(dotenv_path)
connect(host=os.getenv("DB_CONNECTION"))

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_DEPLOYMENT")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(model_router, prefix="/api/model")
app.include_router(chat_router, prefix="/api/chat")
app.include_router(user_router, prefix="/api/user")


@app.get("/")
def read_root():
    return {"message": "Welcome to GenL API"}
