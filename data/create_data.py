import pandas as pd
import numpy as np

def create_table(n=7):
    df = pd.DataFrame({"x": range(1, 11), "y": n})
    df['x*y'] = df.x * df.y
    return df

def get_yahoo_fantasy(session):
     df = session.execute('select * from basketball.yahoo.yahoo_fantasy;').fetch_pandas_all()
     return df