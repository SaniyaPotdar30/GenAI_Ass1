import streamlit as st
import time

st.set_page_config(page_title=" Chatbot Stream", layout="centered")

st.title(" Streamlit Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Generator function for streaming response
def bot_response_stream(text):
    reply = f"You said: {text}"
    for char in reply:
        yield char
        time.sleep(0.05)   # ⏳ typing delay

# Chat input
user_msg = st.chat_input("Type your message...")

if user_msg:
    # Show user message
    st.session_state.messages.append(
        {"role": "human", "content": user_msg}
    )
    with st.chat_message("human"):
        st.write(user_msg)

    # Show bot response with streaming
    with st.chat_message("ai"):
        response = st.write_stream(bot_response_stream(user_msg))

    # Save bot response
    st.session_state.messages.append(
        {"role": "ai", "content": f"You said: {user_msg}"}
    )