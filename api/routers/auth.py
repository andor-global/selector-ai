import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr, validator, constr
from jwt import encode as jwt_encode
import bcrypt
from ..models.user import User
from mongoengine.queryset import DoesNotExist

router = APIRouter()


class LoginInfo(BaseModel):
    email: EmailStr
    password: str


class RegisterInfo(BaseModel):
    name: constr(min_length=3, max_length=256)
    email: EmailStr
    password: constr(min_length=8)
    birth_day: constr(regex=r'\d{4}-\d{2}-\d{2}')
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


@router.post("/login")
async def handle_login(loginInfo: LoginInfo, response: Response):
    try:
        user = await User.objects.get(email=loginInfo.email)
        if bcrypt.checkpw(loginInfo.password.encode('utf-8'), user.password.encode('utf-8')):
            payload = {
                "user_id": user.id,
                "expiration": datetime.now() + timedelta(days=3)
            }

            token = jwt_encode(payload, os.getenv(
                "JWT_SECRET"), algorithm="HS256")

            response.set_cookie(
                key="auth_token",
                value=token,
                samesite='none',
                httponly=True,
                secure=True
            )

            return {"message": "Successful login"}
        else:
            raise DoesNotExist("Wrong password")
    except User.DoesNotExist:
        raise HTTPException(
            status_code=401, detail="Email or Password is incorrect")


@router.post("/register")
async def handle_register(registerInfo: RegisterInfo, response: Response):
    user = User(
        name=registerInfo.name,
        email=registerInfo.email,
        password=registerInfo.password,
        birth_day=registerInfo.birth_day,
        sex=registerInfo.sex
    )

    await user.save()

    payload = {
        "user_id": user.id,
        "expiration": datetime.now() + timedelta(days=3)
    }

    token = jwt_encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
    response.set_cookie(
        key="auth_token",
        value=token,
        samesite='none',
        httponly=True,
        secure=True
    )

    return {"message": "Successful registration"}
