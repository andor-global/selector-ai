import replicate
import streamlit as st
import os

def query(prompt, system_prompt):
    try:
        replicate_ = replicate.Client(api_token=st.secrets['REPLICATE_API_TOKEN'])
        output = replicate_.run(
            "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
            input={"prompt": prompt,
                   "system_prompt": system_prompt
                   })

        answer = ""
        for item in output:
            answer += item
        return answer
    except:
        return ""
