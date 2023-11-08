from fastapi import APIRouter, Depends, Request, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.middleware import verify_auth, validate_image
from ..models.psycho_type import PsychoType

router = APIRouter()

# router.dependencies.append(Depends(verify_auth))


@router.get("/questions")
async def get_questions():
    pass


@router.post("/answers")
async def submit_answers(request: Request, answers: list[str]):
    if len(answers) != 19:
        raise HTTPException("haven't answered all questions")

    fields = list(PsychoType._fields.keys())
    psychoType = PsychoType()

    for i in range(len(answers)):
        psychoType[fields[i]] = answers[i]

    psychoType.save()  # use await if needed later in the code

    # give psychotype answers to AI and get back psychotype answer. then save in user

    return psychoType.to_string()
