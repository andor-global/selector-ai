from fastapi import APIRouter
from pydantic import BaseModel

# from machine_learning import model

router = APIRouter()


class GeneratePrompt(BaseModel):
    sex: str
    age: int


@router.get("/generate")
async def generate_image(prompt: GeneratePrompt):
    # image = await _services.generate_image(imgPrompt=imgPromptCreate)

    # memory_stream = io.BytesIO()
    # image.save(memory_stream, format="PNG")
    # memory_stream.seek(0)
    # return StreamingResponse(memory_stream, media_type="image/png")
    return {"message": "generated image"}
