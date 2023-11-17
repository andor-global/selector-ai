from fastapi import APIRouter, HTTPException, Request, Depends

from ..models.user import User
from ..middleware import validate_http_auth

router = APIRouter()

router.dependencies.append(Depends(validate_http_auth))


@router.get('/')
async def get_authenticated_user(request: Request):
    user = await User.find_one({'_id': request.state.user_id}, exclude=['_id', 'password'])
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    return user
