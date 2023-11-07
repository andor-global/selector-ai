import os
from mongoengine import connect
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path)


async def connect_to_database():
    await connect(os.getenv("DB_CONNECTION"))
    print("Connected to database")
