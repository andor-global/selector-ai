import requests
import os

API_URL = "https://api-inference.huggingface.co/models/swaroopajit/git-base-fashion"
headers = {"Authorization": "Bearer "+os.environ(['HUGGING_FACE_API_KEY'])}

def process_image(image):
    try:
        response = requests.post(API_URL, headers=headers, data=image)
        answer = response.json()[0]['generated_text']
    except:
        answer = ""
    return answer
