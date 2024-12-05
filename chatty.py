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
        
            


        /* General Page Styles */
        .main {
            padding: 2rem;
            max-width: 100%;
            margin: 0 auto;
            font-family: 'Helvetica Neue', sans-serif;
            
        }

        /* Sidebar styles */
        .sidebar .sidebar-content {
            background-color: #F4F6F9;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        .sidebar .sidebar-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2C3E50;
        }

        .sidebar button {
            margin-bottom: 12px;
            font-weight: bold;
            padding: 12px;
            background-color: #3498DB;
            color: white;
            border: none;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }

        .sidebar button:hover {
            background-color: #2980B9;
        }

        /* Chat Messages */
        .chat-message-user, .chat-message-assistant {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 12px;
            max-width: 75%;
            word-wrap: break-word;
            font-size: 1.1rem;
        }

        .chat-message-user {
            background-color: #EAF4FB;
            color: #2C3E50;
        }

        .chat-message-assistant {
            background-color: #DFF0D8;
            color: #2C3E50;
        }

        /* Custom CSS for animation */
        .clean-message {
            font-size: 3rem;
            color: #28A745;
            text-align: center;
            animation: fadeOut 3s ease-in-out;
        }

        @keyframes fadeOut {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 0; }
        }

        /* Search bar animation */
        .search-bar {
            animation: fadeIn 2s ease-in-out;
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        /* About Section */
        .about-section {
            background-color: #F9FAFB;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 1.1rem;
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
    about_button = st.button("About", type="secondary")

    # New features
    st.markdown("---")
    user_profile_button = st.button("User Profile", type="secondary")
    help_button = st.button("Help", type="secondary")
    feedback_button = st.button("Feedback", type="secondary")
    
    # Additional sidebar options
    st.markdown("---")
    if st.button("Clear Chat"):
        # Display "all clear👍" message and reset the chat history
        with st.empty():
            st.markdown("<div class='clean-message'>all clear👍</div>", unsafe_allow_html=True)
        
        # Clear the session state without restarting the app
        st.session_state.chat_session = model.start_chat(history=[])  # Restart the chat session
        
        # No need for st.experimental_rerun(), just refresh the page
        #st.experimental_rerun()  # Ensure the page state is reset

# Main page content
st.title("BGS College of Engineering and Technology")
st.markdown("<hr>", unsafe_allow_html=True)
st.title("🩺CareHub AI Healthcare Diagnosis💊")


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

# Handle new feature interactions

# User Profile Feature
# User Profile Feature
if user_profile_button:
    st.write("🔒 **User Profile**: Manage and update your profile securely with us. We prioritize your privacy and ensure that your personal data is encrypted and protected at all times...")
    
    # Add "Meet the Developers" section
    st.markdown("""
        <div style="margin-top: 2rem;">
            <h3>👨‍💻 Meet the Developers</h3>
            <ul style="font-size: 1.1rem; line-height: 2;">
                <li><strong>ARJUN P GUPTA</strong> - Developer ID: 1MP22CS008</li>
                <li><strong>KIRAN R</strong> - Developer ID: 1MP22CS025</li>
                <li><strong>SANATH S GOWDA</strong> - Developer ID: 1MP22CS046</li>
                <li><strong>SANTOSH S</strong> - Developer ID: 1MP22CS047</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Help Feature
if help_button:
    st.write("💡 **Help**: Here are some helpful tips for using this platform:\n- Type your queries in the input box.\n- Ask for healthcare insights and recommendations.")

# Feedback Feature
if feedback_button:
    st.write("✍️ **Feedback**: Please provide your feedback here:\n- What did you like?\n- What can we improve?")

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
