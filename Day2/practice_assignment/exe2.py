import streamlit as st

with st.form(key="Login form"):
    st.header("Login form")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type = "password")
    submit_button = st.form_submit_button(label = "Login")

if submit_button:
    st.success(f"Successfully logged in!")