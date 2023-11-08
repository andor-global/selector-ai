from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..models.user import User
from ..middleware import verify_auth

router = APIRouter()

router.dependencies.append(Depends(verify_auth))


@router.get('/')
async def get_authenticated_user(request: Request):
    try:
        user = User.objects.only('name', 'email', 'birth_day', 'sex').get(
            id=request.state.user_id)
        return JSONResponse(content=user)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User does not exist")
