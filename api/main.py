import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.connection import connect_to_database
from .routers.auth import router as auth_router
from .routers.model import router as model_router
from .routers.chat import router as chat_router

connect_to_database()

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"message": "Welcome to GenL API"}
