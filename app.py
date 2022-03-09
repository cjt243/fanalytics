import streamlit as st
st.set_page_config(layout="wide")
import json
import pandas as pd
import snowflake.connector
from aws_functions import get_secret

# Setup connection and get data

@st.cache
def get_creds(name,region):
    secret = json.loads(get_secret(name,region))
    return secret

@st.experimental_singleton # magic to cache db connection
def create_connection(secret):
    con = snowflake.connector.connect(
        user=secret["USER"],
        password=secret["PASSWORD"],
        account=secret["ACCOUNT"],
        session_parameters={
            'QUERY_TAG': secret["QUERY_TAG"],
            'ROLE':secret["ROLE"]
    }
)
    return con

secret = get_creds("SNOWFLAKE-SANDBOX","us-east-2")
con = create_connection(secret)

@st.experimental_memo(ttl=600) # 10 minute object cache, or when query changes. Applies to all usage of this func.
def run_query(query):
    with con.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()


cur = con.cursor()
views_df = run_query("select * from information_schema.views where table_schema = 'YAHOO';")

selected_view = st.selectbox('Pick a view',list(views_df["TABLE_NAME"]))

df = run_query(f"select * from YAHOO.{selected_view}")

st.table(df)