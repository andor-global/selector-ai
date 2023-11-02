from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from api.middleware import auth_middleware, validate_image

router = APIRouter()

router.middleware(auth_middleware)


@router.post("/")
async def send_message(message: str):
    chat_bot_response = "This is the response from the chat bot."
    return {"message": chat_bot_response}


@router.post("/img/", dependencies=[Depends(validate_image)])
async def upload_image(image: UploadFile = File(...)):
    # save_uploaded_image(image)
    return {"message": f"Image uploaded by user {image.filename}"}
