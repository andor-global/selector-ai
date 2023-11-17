import os
from contextlib import asynccontextmanager
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .psycho_type import PsychoType
from .user import User

dotenv_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../.env"))
load_dotenv(dotenv_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = AsyncIOMotorClient(os.getenv("DB_CONNECTION")).test
    await init_beanie(app.db, document_models=[User, PsychoType])
    print("Startup complete")
    yield
    print("Shutdown complete")
