from fastapi import APIRouter
from db.models import User

router = APIRouter()


@router.get("/login")
async def handle_login():
    return {"message": "Login"}
