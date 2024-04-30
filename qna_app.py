import streamlit as st
import random
import time

import os

from langchain.callbacks.base import BaseCallbackHandler
from qna_langchain import ask_qa, ask_qa_stream

st.title("Qapita AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def stream_response(chat_id, prompt):
    iterator = ask_qa_stream("vmk_1", prompt, callbacks=[])

    answer = st.write_stream(iterator)
    st.session_state.messages.append({"role": "assistant", "content": answer})

def direct_response(chat_id, prompt):
    response = ask_qa(chat_id, prompt)
    answer = response['answer']
    st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Accept user input
if prompt := st.chat_input("Saarthi here, how can I help?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    # response = ask_qa("vmk_1", prompt)
    # answer = response['answer']
    # st.chat_message("assistant").write(answer)
    with st.chat_message("assistant"):
        stream_response("vmk_1", prompt)
        # direct_response("vmk_1", prompt)


