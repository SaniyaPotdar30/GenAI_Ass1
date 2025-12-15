import pandas as pd
import streamlit as st

st.title("CSV explorer")

data_file = st.file_uploader("Upload CSV file", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)