# Use a pipeline as a high-level helper
from transformers import pipeline
pipe = pipeline("image-to-text", model="swaroopajit/git-base-fashion")

def process_image(image):
    text = pipe(image)
    try:
       image_description = text[0]['generated_text']
    except:
       image_description = ""
    return image_description

#image = Image.open("C:/Users/Aleksandra/genL/machine_learning/example.jpeg")
#text = process_image(image)
#print(text)
