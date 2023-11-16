import os
from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr, validator, constr
from jwt import encode as jwt_encode
import bcrypt
from ..models.user import User
from mongoengine.queryset import DoesNotExist
from mongoengine.errors import NotUniqueError

router = APIRouter()


class LoginInfo(BaseModel):
    email: EmailStr
    password: str


class RegisterInfo(BaseModel):
    name: constr(min_length=3, max_length=256)
    email: EmailStr
    password: constr(min_length=6)
    birth_day: date
    sex: str

    @validator("password")
    def validate_password(cls, value):
        if not any(char.isnumeric() for char in value):
            raise ValueError(
                "Password must contain at least one numeric character")
        if not any(char.isalpha() for char in value):
            raise ValueError(
                "Password must contain at least one alphabetic character")
        return value

    @validator("sex")
    def validate_sex(cls, sex):
        if sex not in ["male", "female"]:
            raise ValueError("Sex is not valid")
        return sex


@router.post("/login", responses={401: {"description": "Item not found"}})
async def handle_login(loginInfo: LoginInfo, response: Response):
    try:
        user = await User.objects.get(email=loginInfo.email)
        if bcrypt.checkpw(loginInfo.password.encode("utf-8"), user.password.encode("utf-8")):
            payload = {
                "user_id": str(user.id),
            }

            token = jwt_encode(payload, os.getenv(
                "JWT_SECRET"), algorithm="HS256")

            response.set_cookie(
                key="auth_token",
                value=token,
                samesite="none",
                secure=True,
                expires=3 * 24 * 60 * 60
            )

            return {"message": "Successful login"}
        else:
            raise DoesNotExist("Wrong password")
    except DoesNotExist:
        raise HTTPException(
            status_code=401, detail="Email or Password is incorrect")


@router.post("/register")
async def handle_register(registerInfo: RegisterInfo, response: Response):
    try:
        user = await User(
            name=registerInfo.name,
            email=registerInfo.email,
            password=registerInfo.password,
            birth_day=registerInfo.birth_day,
            sex=registerInfo.sex
        )

        user.save()

        payload = {
            "user_id": str(user.id),
        }

        token = jwt_encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
        response.set_cookie(
            key="auth_token",
            value=token,
            samesite="none",
            secure=True,
            expires=3 * 24 * 60 * 60
        )

        return {"message": "Successful registration"}
    except NotUniqueError:
        raise HTTPException(status_code=401, detail="Email already exists")
