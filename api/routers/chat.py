from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.middleware import verify_auth, validate_image

router = APIRouter()

router.dependencies.append(Depends(verify_auth))


class ChatAnswer(BaseModel):
    text: Optional[str]
    img: Optional[str]  # base64_encoded_img_file


@router.post("/answers")
async def submit_answers(answers: list[ChatAnswer], img: str = Depends(validate_image)):
    for answer in answers:
        print(answer.text)

    # for image in images:
    #     try:
    #         # Decode Base64-encoded image data
    #         image_data = base64.b64decode(image.data)

    #         # Specify a directory where you want to save the images
    #         upload_dir = "uploads"
    #         os.makedirs(upload_dir, exist_ok=True)

    #         # Save the image to the specified directory
    #         with open(os.path.join(upload_dir, image.filename), "wb") as file:
    #             file.write(image_data)

    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=500, detail=f"Failed to save image {image.filename}: {str(e)}")

    return {"message": "Images uploaded successfully"}
