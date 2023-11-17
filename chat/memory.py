from langchain.memory import ConversationBufferMemory

def create_memory(memory_state={}):
    """
    Creates a ConversationBufferMemory instance for storing conversation context.

    Parameters:
    - memory_state (dict): Optional initial memory state.

    Returns:
    - ConversationBufferMemory: Instance of the memory class for conversation context.
    """
    # Initialize a ConversationBufferMemory instance with the ability to return messages
    memory = ConversationBufferMemory(return_messages=True)

    # Load the provided memory state into the memory instance
    memory.load_memory_variables(memory_state)

    return memory
