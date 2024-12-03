import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import time

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon="🤖",
    layout="wide",  # Use wide layout to utilize the full screen
    initial_sidebar_state="expanded",  # Show sidebar by default
)

# Add custom CSS to enhance styling
st.markdown("""
    <style>
        /* Adjust page layout for full screen usage */
        .main {
            padding: 2rem;
            max-width: 100%;
            margin: 0 auto;
        }

        .sidebar .sidebar-content {
            background-color: #f1f1f1;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        .sidebar .sidebar-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
        }

        .sidebar button {
            margin-bottom: 10px;
            font-weight: bold;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        .sidebar button:hover {
            background-color: #45a049;
        }

        .chat-message-user, .chat-message-assistant {
            font-family: 'Arial', sans-serif;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 10px;
            background-color: #e0f7fa;
            max-width: 80%;
            word-wrap: break-word;
        }

        .chat-message-assistant {
            background-color: #f1f8e9;
        }

        /* Style for the About section */
        .about-section {
            background-color: #f9f9f9;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
        }

        .about-section h2 {
            color: #2C3E50;
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .about-section p {
            color: #34495E;
            line-height: 1.8;
            margin-bottom: 1rem;
        }

        /* Custom CSS for animation */
        .clean-message {
            font-size: 3rem;
            color: green;
            text-align: center;
            animation: fadeOut 3s ease-in-out;
        }

        @keyframes fadeOut {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 0; }
        }

        .search-bar {
            animation: fadeIn 2s ease-in-out;
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# Get the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar navigation
with st.sidebar:
    st.markdown("### ⚙️ Navigation", unsafe_allow_html=True)
    st.markdown("---")
    chat_button = st.button("Chat", type="primary")
    settings_button = st.button("Settings", type="secondary")
    about_button = st.button("About", type="secondary")
    
    # Additional sidebar options
    st.markdown("---")
    if st.button("Clear Chat"):
        # Display clean message and hide chat for a moment
        with st.empty():
            st.markdown("<div class='clean-message'>🧹 Everything clean!</div>", unsafe_allow_html=True)
        
        time.sleep(2)  # Wait for the animation to finish
        st.session_state.chat_session = model.start_chat(history=[])  # Restart the chat session
        st.experimental_rerun()  # Restart the app to reset the state

# Main page content
st.title("🩺CareHub AI Healthcare Diagnosis💊")
st.markdown("<hr>", unsafe_allow_html=True)

# Display "About" section content when About button is clicked
if about_button:
    st.markdown("""
        <div class="about-section">
            <h2>About CareHub AI Healthcare Diagnosis</h2>
            <p>
                **CareHub** is a cutting-edge AI platform designed to revolutionize the healthcare industry. Our AI-powered solutions assist healthcare professionals with diagnosis, predictive analytics, and treatment recommendations.
            </p>
            <p>
                By leveraging machine learning and vast datasets, CareHub provides real-time insights, helping doctors make informed decisions quickly and accurately. Our platform analyzes patient data, detects patterns, and suggests personalized treatment plans to improve patient outcomes.
            </p>
            <p>
                Whether you're a healthcare provider or patient, CareHub makes the process of diagnosis smarter, faster, and more efficient, ultimately improving the quality of care across the globe.
            </p>
            <p>
                With CareHub, healthcare professionals are empowered with the tools they need to provide the best possible care for their patients, enabling a healthier future for all.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
