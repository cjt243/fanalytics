import snowflake.connector
import pandas as pd
import json
from aws_functions import get_secret

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

