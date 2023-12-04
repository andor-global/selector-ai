import os
from pathlib import Path
from typing import Union
from dotenv import load_dotenv
from machine_learning import mistral_model
import json

dotenv_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../.env"))
load_dotenv(dotenv_path)


def load_psychotypes_data():
    with open(Path("./psychotype/psychotypes.json"), 'r') as file:
        data = json.load(file)
        return data


def extract_psychotypes_description(data, gender):
    descriptions = []
    for psychotype in data[gender]:
        descriptions.append(psychotype + " description: " + data[gender][psychotype]["description"])
    return '; '.join(descriptions)


def detect_psychotype(answers: str, gender: str, age: int):
    psychotypes_data = load_psychotypes_data()
    psychotype_descriptions = extract_psychotypes_description(psychotypes_data, gender)

    system_prompt = f'You are an experienced personal stylist. \
                     Here is the psychotypes description: {psychotype_descriptions}.'

    prompt = f"Please, predict the psychotype of the client based on the syrvey answers \
              and give a precise exlanation of your decision. For {gender} of {str(age)} age. Here are the answers: {answers}"

    prompt_template = f"< | im_start | > system\
                      {system_prompt}\
                      < | im_end | >\
                      < | im_start | > user\
                      {prompt} < | im_end | >\
                      < | im_start | > assistant"

    model_params = {
        'prompt_template': prompt_template,
        'prompt': prompt
    }
    model_answer = mistral_model.query(model_params)
    return extract_from_answer(model_answer)


def extract_from_answer(model_answer: str) -> Union[str, None]:
    psycho_types = ['classical', 'expressive', 'dramatic', 'spectacular', 'romantic', 'natural', 'gamine']
    model_answer = model_answer.lower()
    matching_words = filter(lambda word: word in model_answer, psycho_types)
    return next(matching_words, None)
