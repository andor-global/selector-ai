from PIL import Image
from fastapi import WebSocket
import requests
import io
from operator import itemgetter
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.llms import Replicate
from langchain.memory import ConversationBufferMemory


class Chat():
    def __init__(self, memory_state, user_profile_info):
        # Initialize the chatbot with user profile information and memory state
        self.user_profile_info = user_profile_info
        self.memory = self.create_memory(memory_state)
        self.create_stylist_llm_chain()
        self.create_painter_llm_chain()
        self.create_image_generator_chain()

    def create_memory(self, memory_state):
        # Create and return a ConversationBufferMemory instance
        memory = ConversationBufferMemory(return_messages=True)
        memory.load_memory_variables(memory_state)
        return memory

    def create_stylist_llm_chain(self):
        # Create LangChain pipeline for the personal stylist role
        llm_stylist_prompt = PromptTemplate.from_template(
            "I'm {age} years old. I'm a {gender}. My personality description is {psychotype_description}. Please, take into account new additional info: {text}")

        llm_stylist = Replicate(
            model="nateraw/mistral-7b-openorca:7afe21847d582f7811327c903433e29334c31fe861a7cf23c62882b181bacb88",
            model_kwargs={
                "max_new_tokens": 300,
                "prompt_template": "system\nYou are an experienced personal stylist. Given the following description of my personality, please provide me a textual description of the style look. Just a list of items to wear.\n\nuser\n{prompt}\nassistant\n"
            }
        )

        self.chain_stylist = (
            RunnablePassthrough.assign(
                history=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")
            )
            | llm_stylist_prompt
            | llm_stylist
            | {"style_look_description": RunnablePassthrough()}
        )

    def create_painter_llm_chain(self):
        # Create LangChain pipeline for the painter role
        llm_painter_prompt = PromptTemplate.from_template(
            "Here is the style look description: {style_look_description}. Please provide me a textual description of the image of the {gender} of age {age} in such outfit in full height. Just items to paint without background.")
        llm_painter = Replicate(
            model="nateraw/mistral-7b-openorca:7afe21847d582f7811327c903433e29334c31fe861a7cf23c62882b181bacb88",
            model_kwargs={
                "max_new_tokens": 200,
                "prompt_template": "system\nYou are an experienced designer and painter.\n\nuser\n{prompt}\nassistant\n"
            }
        )
        self.chain_painter = (
            llm_painter_prompt
            | llm_painter
            | {"image_description": RunnablePassthrough()}
        )

    def create_image_generator_chain(self):
        # Create LangChain pipeline for generating images from style look descriptions
        image_generator_prompt = PromptTemplate(input_variables=["image_description", "gender", "age"],
                                                template="Realistic photo in a full height if the {gender} of age {age} in the outfit: {image_description}")
        image_generator = Replicate(
            model="stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")
        self.image_generator_chain = (
            image_generator_prompt
            | image_generator
            | {"image_url": RunnablePassthrough()}
        )

    def execute(self, user_input: str) -> dict:
        # Invoke the personal stylist chain to get style look description
        chain_output = self.chain_stylist.invoke({
            'text': user_input,
            'gender': self.user_profile_info['gender'],
            'age': self.user_profile_info['age'],
            'psychotype_description': self.user_profile_info['psychotype_description']
        })

        # Extract style look description from chain output
        style_look_description = chain_output['style_look_description']

        # Invoke the painter chain to get image description
        chain_output = self.chain_painter.invoke({
            'style_look_description': style_look_description,
            'gender': self.user_profile_info['gender'],
            'age': self.user_profile_info['age'],
            'psychotype_description': self.user_profile_info['psychotype_description']
        })

        # Extract image description from chain output
        image_description = chain_output['image_description']

        # Invoke the image generator chain to get image URL
        chain_output = self.image_generator_chain.invoke({
            'image_description': image_description,
            'gender': self.user_profile_info['gender'],
            'age': self.user_profile_info['age'],
        })

        # Extract image URL from chain output
        image_url = chain_output['image_url']

        # Save the conversation context to memory
        self.memory.save_context({"input": user_input}, {"output": style_look_description})

        # Display the bot's response
        return {'style_look_description': style_look_description, 'image_url': image_url}
