import openai
import streamlit as st

openai.api_key = st.secrets["open_ai_api_key"]


def get_style_look_description(personality_description, references_description, goal):
    prompt = f"You are an experienced fashion designer. Given the following description of the personality,\
               please provide a textual description of the style look for the specific goal. Just a set of items, no more.\
               Personality: {personality_description}. Goal: {goal}. References' images descriptions: {references_description}. Please provide me with a description with no more than 77 tokens."

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=78,
        n=1,
        stop=None,
        temperature=0.7
    )

    recommendation = response.choices[0].text.strip()

    return recommendation
