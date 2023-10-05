from PIL import Image

import img2text_clothes
import img2test_general
import chatGPTmodel

def generate_reference_images_description(uploaded_files_info):
    references_descriptions = []

    for idx, file in enumerate(uploaded_files_info):
        if file['type'] == 'Clothes':
            references_descriptions.append(img2text_clothes.process_image(file['file']))
        elif file['type'] == 'Moodboard':
            references_descriptions.append(img2test_general.process_image(file['file']))

    return ', '.join(references_descriptions)


def generate_style_look_description(personality_description, style_goal, uploaded_files_info):
    references_descriptions = generate_reference_images_description(uploaded_files_info)
    try:
        style_look_description = chatGPTmodel.get_style_look_description(personality_description, references_descriptions, style_goal)
    except:
        style_look_description = ""
    return style_look_description


