import os
from chat import Chat

def main(user_profile_info, memory_state={}):
    # Entry point for the chatbot application
    os.environ["REPLICATE_API_TOKEN"] = ...

    # Create an instance of the Chat class and execute the chat loop
    chat = Chat(memory_state={}, user_profile_info = user_profile_info)
    chat.execute()

# Example Usage:
user_profile_info = {'gender': 'female', 'age': '27', 'psychotype_description': 'dramatic'}

main(user_profile_info)
