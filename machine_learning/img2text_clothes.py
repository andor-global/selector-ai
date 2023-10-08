import requests

API_URL = "https://api-inference.huggingface.co/models/swaroopajit/git-base-fashion"
headers = {"Authorization": "Bearer "}

def process_image(image):
    try:
        response = requests.post(API_URL, headers=headers, data=image)
        answer = response.json()[0]['generated_text']
    except:
        answer = ""
    return answer
