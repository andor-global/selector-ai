from PIL import Image
import requests
import os
from chat.chain import create_chain
from chat.memory import create_memory
import io


def chat(user_profile_info, memory_state={}):
    """
    Conducts a chat using the Replicate API and displays information including style descriptions and images.

    Parameters:
    - user_profile_info (dict): User profile information containing gender, age, and psychotype description.
    - memory_state (dict): Optional memory state to initialize the conversation memory.

    Example Usage:
    user_profile_info = {'gender': 'female', 'age': '27', 'psychotype_description': 'dramatic'}
    chat(user_profile_info)
    """

    # Initialize Replicate API token from Streamlit secrets
    os.environ["REPLICATE_API_TOKEN"] = st.secrets['REPLICATE_API_TOKEN']

    # Initialize conversation memory
    memory = create_memory(memory_state={})

    # Create conversation chain
    chain = create_chain(memory)

    # Start the conversation loop
    while True:
        # Get user input from the console
        user_input = input('user: ')

        # Invoke the chain with user input and user profile information
        chain_output = chain.invoke({
            'text': user_input,
            'gender': user_profile_info['gender'],
            'age': user_profile_info['age'],
            'psychotype_description': user_profile_info['psychotype_description']
        })

        # Extract style look description and image URL from chain output
        style_look_description = chain_output['image_description']
        image_url = chain_output['image']

        # Display the bot's response
        print('bot:', style_look_description)

        # Save the conversation context to memory
        memory.save_context({"input": user_input}, {"output": style_look_description})
        print(memory.load_memory_variables({}))

        # Get the image in bytes from the provided URL
        image_bytes = requests.get(image_url).content

        # Convert bytes to a PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image locally
        image.save("images\image.jpg")


# Example Usage:
user_profile_info = {'gender': 'female', 'age': '27', 'psychotype_description': 'dramatic'}
chat(user_profile_info)