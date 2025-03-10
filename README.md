# Streamlit Chat Interface

A web-based chat interface built with Streamlit that connects to an Azure ML endpoint for processing queries.

## Setup Instructions

### 2. Create a Virtual Environment

#### On Windows
```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate
```

#### On macOS/Linux
```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 3. Install Requirements
With the virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Open `streamlit_app.py` and add your Azure ML API key:
```python
api_key = 'your-api-key-here'  # Replace with your actual API key
```

Alternatively, you can use environment variables:
1. Create a `.env` file in the project root
2. Add your API key:
```
API_KEY=your-api-key-here
```

### 5. Run the Application
```bash
streamlit run streamlit_app.py
```
The application will start and open in your default web browser at `http://localhost:8501`

## Features
- Clean, modern chat interface
- Conversation history with timestamps
- Context-aware responses
- Easy-to-use chat input
- Clear chat functionality
- Debug view for conversation context

## Troubleshooting

### Virtual Environment Issues
If you see an error about "activate" not being recognized:
- Make sure you're in the project directory
- Check that the virtual environment was created successfully (you should see a `.venv` directory)
- Try creating the virtual environment again

### Package Installation Issues
If you encounter errors during package installation:
```bash
# Upgrade pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### API Connection Issues
If you get API connection errors:
- Verify your API key is correct
- Check your internet connection
- Ensure the Azure ML endpoint is accessible

## Deactivating the Virtual Environment
When you're done working on the project:
```bash
deactivate
```

## Project Structure
```
├── README.md
├── requirements.txt
├── streamlit_app.py
└── .env (create this file for API key)
```