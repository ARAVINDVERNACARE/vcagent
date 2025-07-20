from logic.sql_generator import generate_sql_query
from db.db_connector import run_sql_query
import pandas as pd

def run_user_query(question: str) -> str:
    try:
        sql = generate_sql_query(question)
        df = run_sql_query(sql)
        if df.empty:
            return "No results found."
        return df.to_string(index=False)
    except Exception as e:
        return f"Error: {str(e)}"

# Toolset for agent
from typing import Callable, Set, Any
user_functions: Set[Callable[..., Any]] = { run_user_query }
