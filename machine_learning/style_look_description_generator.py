from machine_learning import img2test_general, img2text_clothes, llama_model


def generate_reference_images_description(uploaded_files_info):
    references_descriptions = []

    for idx, file in enumerate(uploaded_files_info):
        if file['type'] == 'Clothes':
            references_descriptions.append("Clothes:")
            references_descriptions.append(img2text_clothes.process_image(file['file']))
        elif file['type'] == 'Moodboard':
            references_descriptions.append("Moodboard:")
            references_descriptions.append(img2test_general.process_image(file['file']))

    return ', '.join(references_descriptions)


def generate_style_look_description(age, gender, personality_description_input, eye_color,\
            hair_color, extra_info, style_goal, references_descriptions):
    try:
        style_look_description = llama_model.get_style_look_description(age, gender, personality_description_input, eye_color,\
            hair_color, extra_info, references_descriptions, style_goal)
    except:
        style_look_description = ""

    return style_look_description


