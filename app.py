from flask import Flask, render_template, request, jsonify
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize PandasAI with OpenAI
llm = OpenAI(api_token=os.getenv('OPENAI_API_KEY'), temperature=0.02)

# Load and prepare the DataFrame
@app.before_first_request
def load_data():
    global sdf
    try:
        #filename = 'output_dataframe.csv'
        filename = 'cleaned_ev_stations.csv'
        df = pd.read_csv(filename)
        df = df.select_dtypes(include=["number", "object", "bool"])

        # Select specific columns
        available_columns = ["title", "address", "reviewsCount", "totalScore", "postalCode", "rank"]
        df_small = df[[col for col in available_columns if col in df.columns]]

        # Configure SmartDataframe
        config = {
            "llm": llm,
            "enable_cache": False,
            "use_error_correction_framework": False,
            "cache": None,
            "save_charts": False,
            "save_logs": False,
            "verbose": True,
            "max_retries": 1,
            "use_duckdb": False
        }

        sdf = SmartDataframe(df_small, config=config)
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        sdf = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        if not sdf:
            return jsonify({'error': 'Data not loaded properly'}), 500
            
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        response = sdf.chat(question)
        
        if isinstance(response, dict):
            if 'type' in response and response['type'] == 'plot':
                return jsonify({'response': 'Plot generated successfully'})
            else:
                return jsonify({'response': str(response.get('value', response))})
        else:
            return jsonify({'response': str(response)})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True) 