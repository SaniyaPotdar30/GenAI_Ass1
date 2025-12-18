import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

with st.sidebar:
    st.header("Settings")

    count = st.slider(
        "Message Count (Last N messages)",
        min_value=2,
        max_value=20,
        value=6,
        step=2
    )

    st.subheader("Config")
    st.json({"message_window": count})

st.title("Yelo Chatbot 🤖 ")

display_messages = st.session_state.messages[-count:]

for msg in display_messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

user_input = st.chat_input("Say something...")

if user_input:
   
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    context_to_send = st.session_state.messages[-count:]

    response = llm.invoke(context_to_send)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )

    st.rerun()