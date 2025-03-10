from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def get_llm_response(query):
    try:
        allowSelfSignedHttps(True)

        # Prepare the request data with the correct 'query' field
        data = {
            "query": query
        }
        body = str.encode(json.dumps(data))
        url = 'https://mass-project-xlcvs.eastus.inference.ml.azure.com/score'
        
        # Get API key from environment variable
        api_key = os.environ.get('AZURE_API_KEY')
        
        if not api_key:
            return "Error: API key not configured. Please set AZURE_API_KEY environment variable."

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = response.read()
        
        return result.decode('utf-8')
        
    except urllib.error.HTTPError as error:
        error_message = f"Request failed with status code: {error.code}\n{error.read().decode('utf-8')}"
        return f"Error: {error_message}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    response = get_llm_response(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)