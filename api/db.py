import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .models.psycho_type import PsychoType
from .models.user import User
from .models.generation import Generation

dotenv_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../.env"))
load_dotenv(dotenv_path)

print(os.getenv("DB_NAME"))
print(os.getenv("DB_CONNECTION"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(os.getenv("DB_CONNECTION"))
    app.db = client[os.getenv("DB_NAME")]
    await init_beanie(app.db, document_models=[User, PsychoType, Generation])
    print("Connected to database")
    yield
    client.close()
    print("Closed database connection")
