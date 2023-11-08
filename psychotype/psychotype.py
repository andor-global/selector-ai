from machine_learning import llama_model
import json

def load_psychotypes_data():
    with open('psychotypes.json', 'r') as file:
        data = json.load(file)
    return data

def extract_psychotypes_description(data, gender):
    descriptions = []
    for psychotype in data[gender]:
        descriptions.append(psychotype + " description: " + data[gender][psychotype]["description"])
    return '; '.join(descriptions)

def detect_psychotype(answers, gender, age):
    psychotypes_data = load_psychotypes_data()
    psychotype_descriptions = extract_psychotypes_description(psychotypes_data, gender)

    system_prompt = f'You are an experinced personal stylist. \
                     Here is the psychotypes description: {psychotype_descriptions}" + \
                    ". Please, predict the psychotype of the client based on the syrvey answers\
                     and give a precise exlanation of your decision. For {gender} of {str(age)} age.'
    prompt = answers
    model_answer = llama_model.query(prompt, system_prompt)
    return model_answer

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data
