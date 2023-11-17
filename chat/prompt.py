from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

def create_llm_prompt():
    """
    Creates a LangChain prompt for a personal stylist providing style look descriptions.

    Returns:
    - ChatPromptTemplate: LangChain prompt template for a personal stylist conversation.
    """
    # Define a system message template for the personal stylist role
    system_message_template = (
        "You are an experienced personal stylist. Given the following description of the personality, "
        "please provide a textual description of the style look for the specific goal. Just a set of items, no more."
    )

    # Create a system message prompt template
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)

    # Define a human message template with placeholders for user profile information
    human_message_template = (
        "Age: {age}. Gender: {gender}. "
        "Psychotype description: {psychotype_description}."
        "Please, take into account additional info: {text}"
    )

    # Create a human message prompt template
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)

    # Create a chat prompt template with system message, message history placeholder, and human message
    prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            MessagesPlaceholder(variable_name="history"),
            human_message_prompt
        ]
    )
    return prompt

def create_text2image_prompt():
    """
    Creates a LangChain prompt for generating an image from a style look description.

    Returns:
    - PromptTemplate: LangChain prompt template for generating an image from a style look description.
    """
    # Create a prompt template for generating an image from a style look description
    prompt = PromptTemplate(
        input_variables=["style look description"],
        template="{style look description}",
    )
    return prompt
