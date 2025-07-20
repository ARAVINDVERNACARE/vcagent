import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("PROJECT_ENDPOINT")
)

def generate_sql_query(user_input: str) -> str:
    prompt = f"""
    You are a SQL assistant. Convert this user request into a SQL query:
    
    Request: "{user_input}"
    
    SQL:"""
    response = client.chat.completions.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()
