import streamlit as st
from PIL import Image
import io
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import webbrowser
import requests
from dotenv import load_dotenv
import os
from datetime import date
import subprocess
import pandas as pd
from sklearn.linear_model import LinearRegression
import pywhatkit
import qrcode

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Unified Automation Dashboard",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- LOAD ENVIRONMENT VARIABLES ---
# Create a .env file in the same directory with your keys
# e.g., GEMINI_API_KEY="your_gemini_key"
load_dotenv()

# --- HELPER FUNCTIONS & API CONFIG ---
def configure_gemini():
    """Configures the Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("models/gemini-1.5-flash")
    return None

gemini_model = configure_gemini()


# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
main_choice = st.sidebar.selectbox(
    "Choose a Category",
    [
        "Machine Learning", "Windows", "Python Automation",
        "Agentic AI", "DevOps", "Cloud", "Full-Stack"
    ]
)

sub_choice = None
if main_choice == "Python Automation":
    sub_choice = st.sidebar.selectbox(
        "Select a Task",
        [
            "Send WhatsApp Message", "Send WhatsApp Image", "Send Email", "Send SMS",
            "Make a Phone Call", "QR Code Generator", "Weather Forecast", "Social Media Posting"
        ]
    )
elif main_choice == "DevOps":
    sub_choice = st.sidebar.selectbox("DevOps Tools", ["Jenkins", "Docker", "Kubernetes"])
elif main_choice == "Cloud":
    sub_choice = st.sidebar.selectbox("Cloud Services", ["AWS EC2", "S3 Buckets", "IAM Roles"])
elif main_choice == "Agentic AI":
    sub_choice = st.sidebar.selectbox("AI Projects", ["Finance Chatbot", "Image Classifier", "Emotion Detector"])
elif main_choice == "Full-Stack":
    sub_choice = st.sidebar.selectbox("Stack Components", ["HTML/CSS", "React/Node", "Database"])


# =========================
# MACHINE LEARNING SECTION
# =========================
def machine_learning_section():
    st.header("🧠 Machine Learning Models")
    st.info("Upload your own CSV files to train the models.")

    ml_model = st.selectbox("Select ML Model", [
        "Salary Prediction (Linear Regression)",
        "Startup Profit Prediction (Multiple Linear Regression)",
    ])

    if ml_model == "Salary Prediction (Linear Regression)":
        st.subheader("Salary Prediction using Linear Regression")
        uploaded_file = st.file_uploader("Upload Salary Dataset (CSV)", type="csv")
        if uploaded_file:
            try:
                dataset = pd.read_csv(uploaded_file)
                st.write("Dataset Preview:", dataset.head())
                
                # Assuming columns are 'YearsExperience' and 'Salary'
                if 'YearsExperience' in dataset.columns and 'Salary' in dataset.columns:
                    x = dataset["YearsExperience"].values.reshape(-1, 1)
                    y = dataset["Salary"].values.reshape(-1, 1)
                    
                    model = LinearRegression()
                    model.fit(x, y)
                    
                    years_exp = st.number_input("Enter Years of Experience:", min_value=0.0, max_value=50.0, step=0.1)
                    if st.button("Predict Salary"):
                        prediction = model.predict([[years_exp]])
                        st.success(f"Predicted Salary: ₹ {prediction[0][0]:,.2f}")
                else:
                    st.error("CSV must contain 'YearsExperience' and 'Salary' columns.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif ml_model == "Startup Profit Prediction (Multiple Linear Regression)":
        st.subheader("Startup Profit Prediction")
        uploaded_file = st.file_uploader("Upload 50_Startups Dataset (CSV)", type="csv")
        if uploaded_file:
            try:
                dataset = pd.read_csv(uploaded_file)
                st.write("Dataset Preview:", dataset.head())

                required_cols = ['R&D Spend', 'Administration', 'Marketing Spend', 'State', 'Profit']
                if all(col in dataset.columns for col in required_cols):
                    dataset = pd.get_dummies(dataset, columns=['State'], drop_first=True)
                    
                    # Ensure all possible state columns exist after one-hot encoding
                    state_cols = [col for col in dataset.columns if col.startswith('State_')]
                    feature_cols = ['R&D Spend', 'Administration', 'Marketing Spend'] + state_cols
                    
                    x = dataset[feature_cols]
                    y = dataset['Profit']
                    
                    model = LinearRegression()
                    model.fit(x, y)

                    st.markdown("### Enter Startup Investment Details")
                    rd_spend = st.number_input("R&D Spend (₹)", min_value=0.0, step=1000.0)
                    admin = st.number_input("Administration Spend (₹)", min_value=0.0, step=1000.0)
                    marketing = st.number_input("Marketing Spend (₹)", min_value=0.0, step=1000.0)
                    
                    # Create input data based on the model's features
                    input_data = pd.DataFrame([[rd_spend, admin, marketing]], columns=['R&D Spend', 'Administration', 'Marketing Spend'])
                    for col in state_cols:
                        input_data[col] = 0 # Default to 0

                    if st.button("Predict Profit"):
                        prediction = model.predict(input_data)
                        st.success(f"Predicted Profit: ₹ {prediction[0]:,.2f}")
                else:
                    st.error(f"CSV must contain {required_cols} columns.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# =========================
# WINDOWS COMMAND SECTION
# =========================
def windows_section():
    st.header("🪟 Windows Command Executor (Local)")
    st.warning("This executes commands on the machine where Streamlit is running. Be careful!")
    user_input = st.text_input("Enter a safe Windows command (e.g., dir, ipconfig, whoami)")
    if st.button("Run Command"):
        if user_input.strip():
            try:
                result = subprocess.run(user_input, shell=True, capture_output=True, text=True, check=True)
                st.code(result.stdout, language="bat")
                if result.stderr:
                    st.error("Error Output:")
                    st.code(result.stderr, language="bat")
            except subprocess.CalledProcessError as e:
                st.error(f"Command failed with exit code {e.returncode}")
                st.code(e.stdout, language="bat")
                st.code(e.stderr, language="bat")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a command.")

# =========================
# PYTHON AUTOMATION SECTION
# =========================
def python_automation_section():
    st.header("🐍 Python Automation Tasks")

    if sub_choice == "Send WhatsApp Message":
        st.subheader("Send Instant WhatsApp Message")
        st.warning("This will open WhatsApp Web in a new browser tab. You must be logged in.")
        phone = st.text_input("Enter phone number with country code (e.g., +919876543210)")
        message = st.text_area("Enter your message")
        if st.button("Send Message via Browser"):
            if phone and message:
                try:
                    pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=True)
                    st.success("WhatsApp tab opened. Check your browser to send the message.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide a phone number and a message.")

    elif sub_choice == "Send WhatsApp Image":
        st.subheader("Send WhatsApp Image")
        st.warning("This will open WhatsApp Web in a new browser tab. You must be logged in.")
        phone = st.text_input("Phone Number (with country code)")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        caption = st.text_input("Caption")
        if st.button("Send Image via Browser"):
            if phone and uploaded_image and caption:
                try:
                    # Save the uploaded file temporarily to send it
                    with open("temp_image.png", "wb") as f:
                        f.write(uploaded_image.getbuffer())
                    
                    pywhatkit.sendwhats_image(phone, "temp_image.png", caption)
                    st.success("WhatsApp tab opened. Check your browser to send the image.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide all details.")

    elif sub_choice == "Send Email":
        st.subheader("Send Email via Gmail")
        st.warning("This requires you to set up an 'App Password' for your Google Account. Do not use your main password here.")
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = st.text_input("Receiver Email")
        subject = st.text_input("Subject")
        body = st.text_area("Email Body")
        
        if st.button("Send Email"):
            if sender and password and receiver and subject and body:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = sender
                    msg['To'] = receiver
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(sender, password)
                        smtp.send_message(msg)
                    st.success("Email sent successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Please fill all fields and set credentials in your .env file.")

    elif sub_choice == "Send SMS":
        st.subheader("Send SMS (via Twilio)")
        st.info("Requires a Twilio account. Set credentials in your .env file.")
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        to_number = st.text_input("Recipient Number (e.g., +919876543210)")
        message = st.text_area("Message")
        
        if st.button("Send SMS"):
            if all([account_sid, auth_token, from_number, to_number, message]):
                try:
                    client = Client(account_sid, auth_token)
                    client.messages.create(body=message, from_=from_number, to=to_number)
                    st.success("SMS sent successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide all details and ensure credentials are in .env file.")

    elif sub_choice == "Make a Phone Call":
        st.subheader("Make a Phone Call (via Twilio)")
        st.info("Requires a Twilio account. Set credentials in your .env file.")
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")

        to_number = st.text_input("Your Verified Number on Twilio")
        call_url = st.text_input("URL with TwiML instructions", value="http://demo.twilio.com/docs/voice.xml")
        
        if st.button("Call Now"):
            if all([account_sid, auth_token, from_number, to_number, call_url]):
                try:
                    client = Client(account_sid, auth_token)
                    call = client.calls.create(url=call_url, to=to_number, from_=from_number)
                    st.success(f"Call initiated successfully! SID: {call.sid}")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide all details and ensure credentials are in .env file.")

    elif sub_choice == "QR Code Generator":
        st.subheader("Generate a QR Code")
        data = st.text_input("Enter text or URL to encode")
        if st.button("Generate QR"):
            if data:
                img = qrcode.make(data)
                buf = io.BytesIO()
                img.save(buf)
                buf.seek(0)
                st.image(buf, caption=f"QR Code for: {data}")
            else:
                st.warning("Please enter some data to generate a QR code.")

    elif sub_choice == "Weather Forecast":
        st.subheader("Check the Weather")
        st.info("Requires a free OpenWeatherMap API key. Set it in your .env file.")
        api_key = os.getenv("OPENWEATHER_API_KEY")
        city = st.text_input("Enter City Name", "London")
        if st.button("Get Weather"):
            if api_key and city:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                try:
                    response = requests.get(url).json()
                    if response["cod"] == 200:
                        temp = response['main']['temp']
                        desc = response['weather'][0]['description']
                        st.success(f"The weather in {city} is {temp}°C with {desc}.")
                    else:
                        st.error(f"Could not find weather for {city}. Error: {response.get('message')}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a city and ensure your API key is set in .env.")

    elif sub_choice == "Social Media Posting":
        st.subheader("Social Media Posting")
        st.warning("Direct API posting to social media is complex and requires developer accounts and app reviews. This section is for demonstration only.")
        st.info("For now, you can generate content here and post it manually.")
        post_content = st.text_area("Compose your post content")
        if st.button("Generate Preview"):
            st.markdown("### Post Preview")
            st.write(post_content)

# =========================
# AGENTIC AI SECTION
# =========================
def agentic_ai_section():
    st.header("🤖 Agentic AI with Gemini")
    st.info("Requires a Gemini API key. Set it in your .env file.")
    
    if not gemini_model:
        st.error("Gemini API key not configured. Please add it to your .env file.")
        return

    st.subheader("Finance Education Chatbot")
    st.markdown("Ask me anything about the *Stock Market & Finance*")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is a mutual fund?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Gemini is thinking..."):
                try:
                    full_prompt = f"You are a finance education assistant. Explain this concept in simple, clear terms for a beginner:\n\n{prompt}"
                    response = gemini_model.generate_content(full_prompt)
                    message_placeholder.markdown(response.text)
                except Exception as e:
                    message_placeholder.error(f"An error occurred with the Gemini API: {e}")
            
            st.session_state.messages.append({"role": "assistant", "content": response.text if 'response' in locals() else "Error"})

# =========================
# PLACEHOLDER SECTIONS
# =========================
def placeholder_section(title):
    st.header(f"⚙️ {title}")
    st.info(f"Selected: {sub_choice}")
    st.write(f"This is a placeholder for {title} tools integration.")
    st.write("You can add relevant controls and logic here in the future.")

# =========================
# MAIN ROUTER
# =_=======================
if main_choice == "Machine Learning":
    machine_learning_section()
elif main_choice == "Windows":
    windows_section()
elif main_choice == "Python Automation":
    python_automation_section()
elif main_choice == "Agentic AI":
    agentic_ai_section()
elif main_choice == "DevOps":
    placeholder_section("DevOps")
elif main_choice == "Cloud":
    placeholder_section("Cloud")
elif main_choice == "Full-Stack":
    placeholder_section("Full-Stack")
else:
    st.write("Please select a category from the sidebar.")
