# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

def process_image(image):
    text = pipe(image)
    try:
       image_description = text[0]['generated_text']
    except:
       image_description = ""
    return image_description
