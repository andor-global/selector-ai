import replicate
import streamlit as st
import os
os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_API_TOKEN']
def get_style_look_description(personality_description, references_description, goal):
    prompt = f"Given the following description of the personality,\
               please provide a textual description of the style look for the specific goal. Just a set of items, no more.\
               Personality: {personality_description}. Goal: {goal}. References' images descriptions: {references_description}."

    output = replicate.run(
        "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
        input={"prompt": prompt,
               "system_prompt": "You are an experienced fashion designer. I need list of items without any introduction.",
               "max_new_tokens": 1000})

    answer = ""
    for item in output:
        answer += item
    print(answer)

    return answer