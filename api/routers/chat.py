from fastapi import APIRouter, Depends, Request, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.middleware import verify_auth, validate_image
from psychotype.psychotype import detect_psychotype
from ..models.psycho_type import PsychoType, get_questions_list
from ..models.user import User

router = APIRouter()

router.dependencies.append(Depends(verify_auth))


@router.get("/questions")
async def get_questions():
    return get_questions_list()


@router.post("/answers")
async def submit_answers(request: Request, answers: list[str]):
    if len(answers) != 19:
        raise HTTPException("haven't answered all questions")

    user = await User.get_user_by_id(request.state.user_id)

    fields = list(PsychoType._fields.keys())
    psychoType = PsychoType(user=user)

    for i in range(len(answers)):
        psychoType[fields[i + 1]] = answers[i]

    psychoType.save()

    user.psycho_type = detect_psychotype(answers, user.sex, user.get_age())
    user.save()

    return psychoType.to_string()
