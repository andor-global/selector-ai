from fastapi import APIRouter, Depends, Request, HTTPException

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

    user = await User.get(request.state.user_id)

    psychoType = PsychoType(user=user)
    fields = list(psychoType.model_dump().keys())[2:]

    for i in range(len(answers)):
        setattr(psychoType, fields[i], answers[i])

    await psychoType.save()

    detected_type = detect_psychotype(psychoType.to_string(), user.sex, user.get_age())
    user.psycho_type = detected_type
    await user.save()

    return {"message": detected_type}
