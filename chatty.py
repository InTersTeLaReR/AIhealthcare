import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import time
from PIL import Image
import pytesseract
import pytesseract

# Replace with the full path to your Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
    products_button = st.button("Products", type="secondary")
    contact_us_button = st.button("Contact Us", type="secondary")
    
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
        
# Main page content
st.title("BGS College of Engineering and Technology")
st.markdown("<hr>", unsafe_allow_html=True)
st.title("🩺CareHub AI Healthcare Diagnosis💊")

# Display the "About" section content when About button is clicked
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

# Display the "Products" section content when Products button is clicked
if products_button:
    st.markdown("""
        <div class="about-section">
            <h2>Our Products</h2>
            <p>
               CareHub is at the forefront of transforming healthcare through artificial intelligence. Our suite of cutting-edge AI software products is designed to enhance diagnostic precision, improve patient outcomes, and streamline healthcare processes. With advanced machine learning models and intelligent algorithms, CareHub empowers healthcare professionals to make faster, more informed decisions, while providing patients with accurate and timely health insights.
            </p>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>AI Diagnostic Assistant:</strong> A tool that assists doctors in diagnosing diseases quickly and accurately.</li>
                <li><strong>Predictive Analytics:</strong> Predicts potential health risks based on patient history and real-time data.</li>
                <li><strong>Smart Treatment Plans:</strong> Suggests personalized treatment plans based on current medical guidelines and patient data.</li>
                <li><strong>Patient Monitoring System:</strong> Continuously tracks patient health metrics through wearable devices and alerts healthcare providers in case of critical events.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Display the "Contact Us" section content when Contact Us button is clicked
if contact_us_button:
    st.markdown("""
        <div class="about-section">
            <h2>Contact Us</h2>
            <p>
                Have questions or need support? Reach out to us through carehubai2024@gmail.com:
            </p>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>Email:</strong> support@carehub.ai</li>
                <li><strong>Phone:</strong> +1 (123) 456-7890</li>
                <li><strong>Website:</strong> www.carehub.ai</li>
                <li><strong>Address:</strong> 123 Health Ave, City, State, ZIP</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Handle new feature interactions

# User Profile Feature
if user_profile_button:
    st.write("🔒 **User Profile**: Manage and update your profile securely with us. We prioritize your privacy and ensure that your personal data is encrypted and protected at all times...")

# Help Feature
if help_button:
    st.write("💡 **Help**: Here are some helpful tips for using this platform:\n- Type your queries in the input box.\n- Ask for healthcare insights and recommendations.")

# Feedback Feature
if feedback_button:
    st.write("✍️ **Feedback**: Please provide your feedback here:\n- What did you like?\n- What can we improve?")

# Image Upload for Prescription Analysis
st.markdown("### 📸 Upload Prescription Photo for Analysis")
uploaded_file = st.file_uploader("Choose a prescription photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Prescription", use_column_width=True)
    
    # Process the image using OCR
    st.write("🔍 Analyzing prescription...")
    
    # Perform OCR to extract text from the image
    extracted_text = pytesseract.image_to_string(image)
    
    # Display extracted text
    st.write("### Extracted Text from Prescription:")
    st.text_area("Extracted Text", value=extracted_text, height=150)
    
    # Send the extracted text to Gemini-Pro for analysis
    if extracted_text.strip():
        gemini_response = st.session_state.chat_session.send_message(extracted_text)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    else:
        st.write("No text could be extracted from the image. Please check the image quality.")
    
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
