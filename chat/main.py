import os
from chat import Chat
from dotenv import load_dotenv

# Entry point for the chatbot application
dotenv_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../.env"))
load_dotenv(dotenv_path)

def main(user_profile_info, memory_state={}):

    os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

    # Create an instance of the Chat class and execute the chat loop
    chat = Chat(memory_state={}, user_profile_info = user_profile_info)
    chat.execute()

# Example Usage:
user_profile_info = {'gender': 'female', 'age': '27', 'psychotype_description': 'dramatic'}

main(user_profile_info)
