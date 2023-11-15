from mongoengine import Document
import json
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request, Depends
from ..middleware import verify_auth

router = APIRouter()

router.dependencies.append(Depends(verify_auth))


@router.get('/')
async def get_authenticated_user(request: Request):
    try:
        user = await User.objects.exclude('password').get(
            id=ObjectId(request.state.user_id))
        user_dict = user.to_mongo().to_dict()
        user_dict.pop("_id", None)
        return user_dict
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User does not exist")
