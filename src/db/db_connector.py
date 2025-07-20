import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

def run_sql_query(query: str) -> pd.DataFrame:
    with engine.begin() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df
