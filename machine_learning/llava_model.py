import replicate
import streamlit as st
import os
os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_API_TOKEN']

def get_style_look_description(age, gender, personality_description,\
            hair_color, extra_info, references_clothes_image, goal, moodboard_description):
    try:
        if references_clothes_image != None:
            prompt = f"Given the following description of the personality,\
                       please provide a textual description of the style look for the specific goal. Just a set of items, no more.\
                       Age: {age}. Gengder: {gender}. Hair color: {hair_color}. \
                       Personality: {personality_description}. \
                       Extra information: {extra_info}. Moodboard description: {moodboard_description}.\
                       PLease, take into account clothes from the image.\
                       Goal: {goal}."

            output = replicate.run(
                "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
                input={"image": references_clothes_image,
                       "prompt": prompt,
                       "system_prompt": "You are an experienced fashion designer. I need list of items to create the overall look."
                       })
        else:
            prompt = f"Given the following description of the personality,\
                       please provide a textual description of the style look for the specific goal. Just a set of items, no more.\
                       Age: {age}. Gengder: {gender}. Hair color: {hair_color}. \
                       Personality: {personality_description}. Extra information: {extra_info}.\
                       Goal: {goal}."

            output = replicate.run(
                "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
                input={"prompt": prompt,
                       "system_prompt": "You are an experienced fashion designer. I need list of items to create the overall look."
                       })

        style_look_description = ""
        for item in output:
            style_look_description += item

        print(style_look_description)
    except:
        style_look_description = ""

    return style_look_description
