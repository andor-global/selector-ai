from langchain.prompts import (
    PromptTemplate
)

def create_llm_stylist_prompt():
    """
    Creates a LangChain prompt for a personal stylist providing style look descriptions.

    Returns:
    - ChatPromptTemplate: LangChain prompt template for a personal stylist conversation.
    """
    # Define a system message template for the personal stylist role
    prompt = PromptTemplate.from_template("I'm {age} years old. I'm a {gender}. My personality description is {psychotype_description}. Please, take into account new additional info: {text}")

    return prompt

def create_llm_painter_prompt():
    """
    Creates a LangChain prompt for a personal stylist providing style look descriptions.

    Returns:
    - ChatPromptTemplate: LangChain prompt template for a personal stylist conversation.
    """
    # Define a system message template for the personal stylist role
    prompt = PromptTemplate.from_template("Here is teh style look description: {style_look_description}. Please provide me a textual description of the person in such clothes.")

    return prompt

def create_text2image_prompt():
    """
    Creates a LangChain prompt for generating an image from a style look description.

    Returns:
    - PromptTemplate: LangChain prompt template for generating an image from a style look description.
    """
    # Create a prompt template for generating an image from a style look description
    prompt = PromptTemplate(
        input_variables=["image_description"],
        template="{image_description}",
    )
    return prompt
