import replicate
import streamlit as st
import os
os.environ['REPLICATE_API_TOKEN'] = st.secrets['REPLICATE_API_TOKEN']
def get_style_look_description(personality_description, references_description, goal):
    prompt = f"Given the following description of the personality,\
               please provide a textual description of the style look for the specific goal. Just a set of items, no more.\
               Personality: {personality_description}. Goal: {goal}. References' images descriptions: {references_description}. Please provide me with a description with no more than 77 tokens."

    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={"prompt": prompt,
               "system_prompt": "You are an experienced fashion designer. I need list of items without any introduction.",
               "max_new_tokens": 100})

    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    answer = ""
    for item in output:
        answer += item
    print(answer)

    return answer