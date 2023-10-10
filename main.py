from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from ml.prototype import obtain_image


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personality Style App API"}


@app.post("/generate_style_look/")
def generate_style_look():
    # Implement the style look generation logic here
    # Return the generated data as a JSON response
    return {"style_look_description": "Generated description", "style_look_image": "image_url"}


@app.get("/generate/")
def generate_image(prompt: str):
    image = obtain_image(prompt,num_inference_steps=5, seed=1024)
    image.save("image.png")
    return FileResponse("image.png")
    # return {"prompt" : prompt}
