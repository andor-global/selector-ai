import streamlit as st
import requests
import numpy as np
import base64
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/mattmdjaga/segformer_b2_clothes"
headers = {"Authorization": "Bearer "+st.secrets["hugging_face_api_key"]}

def mask_to_bool_tensor(mask_base64):
    # Decode the base64 string into bytes
    mask_bytes = base64.b64decode(mask_base64)

    # Read the bytes as an image
    image = Image.open(io.BytesIO(mask_bytes))

    # Convert the image to a NumPy array
    mask_array = np.array(image)

    # Convert the mask array to a boolean array
    bool_mask_array = mask_array.astype(bool)

    return bool_mask_array
clothes_classes_dict = {
    "Background": 0,
    "Hat": 1,
    "Hair": 2,
    "Sunglasses": 3,
    "Upper-clothes": 4,
    "Skirt": 5,
    "Pants": 6,
    "Dress": 7,
    "Belt": 8,
    "Left-shoe": 9,
    "Right-shoe": 10,
    "Face": 11,
    "Left-leg": 12,
    "Right-leg": 13,
    "Left-arm": 14,
    "Right-arm": 15,
    "Bag": 16,
    "Scarf": 17
}

clothes_classes_list = [1,3,4,5,6,7,8,9,10,17,16]
def get_bounding_boxes(data):
    try:
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    except:
        return None

def create_bounding_box(mask, threshold=0.8):
    # Find the coordinates of the bounding box
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]

    return (xmin, ymin, xmax, ymax)

def crop_image(image, bounding_box):
    xmin, ymin, xmax, ymax = bounding_box
    cropped_image = image.crop((xmin, ymin, xmax, ymax))
    return cropped_image


def get_clothes_images(image_bytes):
    pred_seg = get_bounding_boxes(image_bytes)
    image_pil = Image.open(image_bytes)
    cloth_images = []
    cloth_classes = []
    for item in pred_seg:
        # Extract the upper cloth mask
        cloth_label = clothes_classes_dict.get(item['label'])
        if cloth_label in clothes_classes_list:
            cloth_mask = mask_to_bool_tensor(item['mask'])
            bbox = create_bounding_box(cloth_mask)
            cloth_image = crop_image(image_pil, bbox)
            cloth_images.append(cloth_image)
            cloth_classes.append(item['label'])
    return cloth_images, cloth_classes

