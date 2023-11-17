from fastapi import APIRouter, Depends, Request, HTTPException
from bson import ObjectId

from api.middleware import validate_http_auth
from psychotype.psychotype import detect_psychotype
from ..models.psycho_type import PsychoType, get_questions_list
from ..models.user import User

router = APIRouter()

router.dependencies.append(Depends(validate_http_auth))


@router.get("/questions")
async def get_questions():
    return get_questions_list()


@router.post("/answers")
async def submit_answers(request: Request, answers: list[str]):
    if len(answers) != 19:
        raise HTTPException(status_code=401, detail="haven't answered all questions")

    user = await User.get(ObjectId(request.state.user_id))

    fields = list(PsychoType.model_dump().keys())
    psychoType = PsychoType(user=user)

    for i in range(len(answers)):
        psychoType[fields[i + 1]] = answers[i]

    psychoType.save()

    user.psycho_type = detect_psychotype(answers, user.sex, user.get_age())
    user.save()

    return {"message": "Successful"}
