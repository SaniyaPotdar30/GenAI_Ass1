import streamlit as st

st.title("Hello, Streamlit!!")
st.header("Welcome to GenAI era..")
st.write("Hello everyone I hope all is well here.")

if st.button("Click here!",type="primary"):
    st.toast("You have successfully clicked a button")
