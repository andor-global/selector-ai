import os
import streamlit as st
import requests

os.environ["REPLICATE_API_TOKEN"] = st.secrets['REPLICATE_API_TOKEN']

from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# llm_prompt = PromptTemplate.from_template(
# )

from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

template="You are experineced personal stylist. Given the following description of the personality, \
please provide a textual description of the style look for the specific goal. Just a set of items, no more. "
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template="Age: {age}. Gengder: {gender}. \
                Psychotype description: {psychotype_description}.\
                Please, take into account additional info: {text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

llm_prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        MessagesPlaceholder(variable_name="history"),
        human_message_prompt
    ]
)

from langchain.llms import Replicate
llm = Replicate(model="meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e")

from operator import itemgetter
memory = ConversationBufferMemory(return_messages=True)
memory.load_memory_variables({})

llm_chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | llm_prompt
    | llm
)

image_prompt = PromptTemplate(
    input_variables=["style look description"],
    template="{style look description}",
)
text2image = Replicate(model="stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")

from langchain.schema.runnable import RunnablePassthrough

image_chain = image_prompt | text2image

final_chain = {"style look description": llm_chain} | RunnablePassthrough.assign(image=image_chain)

from PIL import Image
import io

# hard code user info
gender = 'female'
age = '27'
psychotype_description = 'dramatic'

while(True):
    user_input = input('user: ')

    # run the chain
    chain_output = final_chain.invoke({'text': user_input, 'gender': gender, 'age': age, 'psychotype_description': psychotype_description})

    # parse the output
    style_look_description = chain_output['style look description']
    image_url = chain_output['image']

    print('bot :', style_look_description)

    # update llm_chain history
    memory.save_context({"input": user_input}, {"output": style_look_description})
    print(memory.load_memory_variables({}))

    # get the image in bytes
    image_bytes = (requests.get(image_url)).content
    # convert to PIL
    image = Image.open(io.BytesIO(image_bytes))
    # save image locally
    image.save("image.jpg")