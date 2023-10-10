from PIL import Image
import io
import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer "+st.secrets["hugging_face_api_key"]}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def generate_style_look_picture(prompt):
    image_bytes = query({
        "inputs": prompt,
    })
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except:
        image = None
    return image