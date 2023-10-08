import requests
import os

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer "+os.environ.get('HUGGING_FACE_API_KEY')}

def process_image(image):
    try:
        response = requests.post(API_URL, headers=headers, data=image)
        answer = response.json()[0]['generated_text']
    except:
        answer = ""
    return answer
