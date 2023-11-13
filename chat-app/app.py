import streamlit as st
import requests
from firebase import firebase  # Install the `python-firebase` library

# Initialize Firebase
firebase_app = firebase.FirebaseApplication('https://your-firebase-app.firebaseio.com/', None)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add a nice background color
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("D:/Git Hub Projects/Realtime-Message-Translator/background.jpg");
    background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Define a simple chat storage
chat_log = []

# Streamlit app title
st.title("Chat App with Translation")

# Create a two-column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sender")

with col2:
    st.subheader("Receiver")

# Language selection for sender
with col1:
    sender_language = st.selectbox("Select Your Language:", ["en", "es", "fr", "si", "ta"])

# Language selection for receiver
with col2:
    receiver_language = st.selectbox("Select Receiver's Language:", ["en", "es", "fr", "si", "ta"])

# User message input for sender
with col1:
    user_message = st.text_area("Your Message (Sender):")

# Translation API (MyMemory) endpoint
translation_url = "https://mymemory.translated.net/api/get"

with col1:
    # Translate user message for sender and display in receiver's text box
    if st.button("Send (Sender)"):
        if user_message:
            response = requests.get(
                translation_url, params={"q": user_message, "langpair": f"{sender_language}|{receiver_language}"}
            )
            translation = response.json().get("responseData", {}).get("translatedText", user_message)

            # Save the message to Firebase
            firebase_app.post('/chat_log', {"user": user_message, "translation": translation, "sender": True})

# Display chat log for sender in the left column
with col1:
    # Retrieve messages from Firebase
    messages = firebase_app.get('/chat_log', None)
    for key, message in messages.items():
        if message["sender"]:
            st.text(f"You (Sender): {message['user']} (in {sender_language})")
            st.text(f"Recipient: {message['translation']} (in {receiver_language})")

# Reply to sender's message for receiver
with col2:
    user_message_receiver = st.text_area("Your Reply (Receiver):")

with col2:
    # Translate user message for receiver and display in sender's text box
    if st.button("Send (Receiver)"):
        if user_message_receiver:
            response = requests.get(
                translation_url, params={"q": user_message_receiver, "langpair": f"{receiver_language}|{sender_language}"}
            )
            translation = response.json().get("responseData", {}).get("translatedText", user_message_receiver)

            # Save the message to Firebase
            firebase_app.post('/chat_log', {"user": user_message_receiver, "translation": translation, "sender": False})

# Display chat log for receiver in the right column
with col2:
    # Retrieve messages from Firebase
    messages = firebase_app.get('/chat_log', None)
    for key, message in messages.items():
        if not message["sender"]:
            st.text(f"You (Receiver): {message['user']} (in {receiver_language})")
            st.text(f"Sender: {message['translation']} (in {sender_language})")
