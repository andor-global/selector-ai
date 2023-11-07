from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, validator, constr
from ..db.models import User

router = APIRouter()


class LoginInfo(BaseModel):
    email: EmailStr
    password: str


class RegisterInfo(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    birth_day: str
    skin_color: str
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


@router.post("/login")
async def handle_login(loginInfo: LoginInfo):
    pass


@router.post("/register")
async def handle_register(registerInfo: RegisterInfo):
    pass
