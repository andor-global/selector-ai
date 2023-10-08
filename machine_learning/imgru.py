import base64
import requests
from io import BytesIO
import streamlit as st

def create_url(image):
    # Set API endpoint and headers
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": "Client-ID "+st.secrets["imgur_cliend_id"]}

    # Read image file and encode as base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    base64_data = base64.b64encode(buffered.getvalue())

    # Upload image to Imgur and get URL
    response = requests.post(url, headers=headers, data={"image": base64_data})
    url = response.json()["data"]["link"]

    return url