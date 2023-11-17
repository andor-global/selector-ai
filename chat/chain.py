from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.llms import Replicate

from operator import itemgetter
from chat.prompt import create_llm_prompt, create_text2image_prompt

def create_llm_chain(memory):
    """
    Creates a LangChain pipeline for the personal stylist role.

    Parameters:
    - memory: ConversationBufferMemory instance for storing conversation context.

    Returns:
    - RunnablePassthrough: LangChain pipeline for the personal stylist role.
    """
    # Initialize the LangChain prompt for personal stylist
    llm_prompt = create_llm_prompt()

    # Initialize the Replicate LLM model for generating style look descriptions
    llm = Replicate(model="meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e")

    # Create a LangChain pipeline
    chain = (
        # Let the chain use memory data
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | llm_prompt
        | llm
    )
    return chain

def create_text2image_chain():
    """
    Creates a LangChain pipeline for generating images from style look descriptions.

    Returns:
    - RunnablePassthrough: LangChain pipeline for generating images from style look descriptions.
    """
    # Initialize the LangChain prompt for text-to-image conversion
    prompt = create_text2image_prompt()

    # Initialize the Replicate LLM model for text-to-image conversion
    text2image = Replicate(model="stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")

    # Create a LangChain pipeline
    image_chain = prompt | text2image

    return image_chain

def create_chain(memory):
    """
    Creates a combined LangChain pipeline using the personal stylist and text-to-image conversion chains.

    Parameters:
    - memory: ConversationBufferMemory instance for storing conversation context.

    Returns:
    - dict: Combined LangChain pipeline with keys representing different roles.
    """
    # Create the personal stylist and text-to-image conversion chains
    llm_chain = create_llm_chain(memory)
    text2image_chain = create_text2image_chain()

    # Combine the chains into a single LangChain pipeline
    chain = {"style look description": llm_chain} | RunnablePassthrough.assign(image=text2image_chain)

    return chain
