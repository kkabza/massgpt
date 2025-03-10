import streamlit as st
import urllib.request
import json
import os
import ssl
from datetime import datetime

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def format_conversation_history(messages):
    # Format the conversation history into a single string
    conversation = ""
    for msg in messages:
        role = "Human" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"
    return conversation

def get_llm_response(query, conversation_history):
    try:
        allowSelfSignedHttps(True)

        # Include the conversation history in the query
        full_context = f"{conversation_history}\nHuman: {query}"
        
        data = {
            "query": full_context
        }
        body = str.encode(json.dumps(data))
        url = 'https://mass-project-xlcvs.eastus.inference.ml.azure.com/score'
        
        # Replace with your API key
        api_key = 'CnPRZ1EyRgwbtJEJNYXiArOlndlIjW41DNEYx9eKbs5nJij9o3iRJQQJ99BBAAAAAAAAAAAAINFRAZML29IY'  # Add your API key here
        
        if not api_key:
            return "Error: API key not configured"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = response.read()
        
        # Parse JSON response
        json_response = json.loads(result)
        return json_response.get('output', 'No output found in response')
        
    except urllib.error.HTTPError as error:
        error_message = f"Request failed with status code: {error.code}\n{error.read().decode('utf-8')}"
        return f"Error: {error_message}"
    except Exception as e:
        return f"Error: {str(e)}"

# Set page config
st.set_page_config(
    page_title="Chat Interface",
    page_icon="💬",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .css-1hynsf2 {
        font-family: 'Arial', sans-serif;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e7f0fe;
    }
    .assistant-message {
        background-color: #f0f2f6;
    }
    .message-timestamp {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("💬 Chat Interface")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-timestamp">{message["timestamp"]}</div>
                    <div>You: {message["content"]}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="message-timestamp">{message["timestamp"]}</div>
                    <div>Assistant: {message["content"]}</div>
                </div>
            """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    # Format conversation history
    conversation_history = format_conversation_history(st.session_state.messages)

    # Get AI response with conversation history
    response = get_llm_response(prompt, conversation_history)

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    # Rerun to update the chat display
    st.rerun()

# Add a clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Optional: Display conversation context (for debugging)
with st.expander("View Conversation Context"):
    if st.session_state.messages:
        st.text(format_conversation_history(st.session_state.messages))