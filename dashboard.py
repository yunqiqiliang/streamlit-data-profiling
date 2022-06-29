import streamlit as st
import snowflake.connector
import pandas as pd
# from credentials import sf_credentials

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"],insecure_mode=True)   
con = init_connection()


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with con.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()

table_name = st.text_input("Enter Table Name", type = "default")


if table_name:
    # sf_table = "JAMIN_TEST.PUBLIC.SALES_TALEND_CREATE"
    query = f"select * from {table_name}"
    df = run_query(query)
    # st.write(st.secrets["user"])
    # building streamlit app
    st.title('Data Profiling Dashboard')
    st.write('Preview:')
    st.write(df.head())

    # length of the table
    columns_length = len(df.columns)
    row_length = len(df)

    # shape
    st.write(f"Table has {columns_length} columns * {row_length} rows")

    # table status
    st.write("#### Table Status")
    st.write(df.describe(include="all").fillna("").astype("str"))

    st.write("#### Null Value")
    st.write(df.isnull().sum())

    st.write("#### Duplicate Value")
    st.write("Table has", df.duplicated().sum(), " duplicated rows")
    st.write(df[df.duplicated()])


    # distribution graph
    st.write("#### Distribution graph for all categorical col")
    col_list = df.select_dtypes(include="object_").columns
    for col in col_list:
        st.bar_chart(df[col].value_counts())

else:
    st.warning('Please input a table')