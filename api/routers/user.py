from fastapi import APIRouter, HTTPException, Request, Depends

from ..models.user import User
from ..middleware import validate_http_auth

router = APIRouter()

router.dependencies.append(Depends(validate_http_auth))


@router.get('/')
async def get_authenticated_user(request: Request):
    user = await User.get(request.state.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    return user
