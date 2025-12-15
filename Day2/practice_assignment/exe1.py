import pandas as pd
import streamlit as st
import pandasql as ps

st.title("CSV Explorer with SQL Query")

# Upload CSV file
data_file = st.file_uploader("Upload CSV file", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)

    st.subheader("Uploaded CSV Data")
    st.dataframe(df)

    # SQL query input
    query = st.text_area(
        "Enter SQL query",
        "SELECT * FROM df"
    )

    if st.button("Execute Query"):
        try:
            result = ps.sqldf(query, {"df": df})
            st.subheader("Query Result")
            st.dataframe(result)
