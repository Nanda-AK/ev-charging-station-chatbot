import pandas as pd
import json
from pandas import json_normalize
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from pandasai import SmartDataframe
from pandasai.llm import OpenAI

llm = OpenAI(api_token=os.getenv('OPENAI_API_KEY'), temperature=0.02)

#filename = 'output_dataframe.csv'
filename = 'cleaned_ev_stations.csv'
df = pd.read_csv(filename)

# Optional: preview
df.head()

df = df.select_dtypes(include=["number", "object", "bool"])

# Select only columns that exist in the DataFrame
#available_columns = ["title", "address", "reviewsCount", "totalScore", "postalCode", "reviews", "rank"]
available_columns = ["title", "address", "reviewsCount", "totalScore", "postalCode", "rank", "review_snippets"]
df_small = df[[col for col in available_columns if col in df.columns]]

# Simple configuration without cache
config = {
    "llm": llm,
    "enable_cache": False,
    "use_error_correction_framework": False,
    "cache": None,  # Explicitly set cache to None
    "save_charts": False,  # Disable chart saving
    "save_logs": False,  # Disable log saving
    "verbose": True,  # Disable verbose output
    "max_retries": 1,  # Limit retries
    "use_duckdb": False  # Disable duckdb
}

sdf = SmartDataframe(df_small, config=config)

while True:
    question = input("Enter your question: ")

    try:
        response = sdf.chat(question)
        if isinstance(response, dict):
            if 'type' in response and response['type'] == 'plot':
                print("Plot generated successfully")
            else:
                print(response.get('value', response))
        else:
            print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        continue