import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer "+st.secrets["hugging_face_api_key"]}

def process_image(image):
    try:
        response = requests.post(API_URL, headers=headers, data=image)
        answer = response.json()[0]['generated_text']
    except:
        answer = ""
    return answer
