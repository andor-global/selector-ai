from PIL import Image
import io
import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer "+st.secrets["hugging_face_api_key"]}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def generate_look(age, gender, hair_color, style_look_description):
    prompt = f"Age: {age}. Gender: {gender}. Hair color: {hair_color}. {style_look_description}"
    image_bytes = query({
        "inputs": prompt,
    })
    try:
        image = io.BytesIO(image_bytes)
    except:
        image = None
    print("pic generated")
    return image