import os
import bcrypt
from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr, validator, constr
from jwt import encode as jwt_encode
from ..models.user import User

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


@router.post("/login")
async def handle_login(loginInfo: LoginInfo, response: Response):
    try:
        user = await User.find_one({'email': loginInfo.email})

        if not user:
            raise Exception("Email doesn't exist")

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

            return {"message": "Successful login", "auth_token": token}
        else:
            raise Exception("Wrong password")
    except Exception:
        raise HTTPException(
            status_code=401, detail="Email or Password is incorrect")


@router.post("/register")
async def handle_register(registerInfo: RegisterInfo, response: Response):
    user = await User.find_one(User.email == registerInfo.email)

    if user != None:
        raise HTTPException(status_code=401, detail="Email already exists")

    hashed_password = bcrypt.hashpw(registerInfo.password.encode('utf-8'), bcrypt.gensalt())

    user = User(
        name=registerInfo.name,
        email=registerInfo.email,
        password=hashed_password.decode('utf-8'),
        birth_day=registerInfo.birth_day,
        sex=registerInfo.sex,
        psycho_type=None
    )

    await user.save()

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

    return {"message": "Successful registration", "auth_token": token}


@router.post("/logout")
async def logout(response: Response):
    response.set_cookie(
        key="auth_token",
        value="",
        samesite="none",
        secure=True,
        expires=0,
    )

    return {"message": "Sucessful logout"}
