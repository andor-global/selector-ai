import utils
import streamlit as st
from streaming import StreamHandler
from langchain.llms import Replicate
from langchain.chains import ConversationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferWindowMemory
import os

class ContextChatbot:

    def __init__(self):
        os.environ["REPLICATE_API_TOKEN"] = st.secrets['REPLICATE_API_TOKEN']
        self.llm_model = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"

    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferWindowMemory(k=5)
        memory.load_memory_variables({})
        llm = Replicate(
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            model=_self.llm_model,
            model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1},
        )
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain

    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                response = chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()