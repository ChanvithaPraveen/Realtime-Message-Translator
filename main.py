# *****************************************************************

import streamlit as st
import requests
import firebase_admin
from firebase_admin import db, credentials

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add a nice background color
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1620121692029-d088224ddc74?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
}
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Mapping dictionary for language codes to names
language_names = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "si": "Sinhala",
    "ta": "Tamil",
    "cn": "Chinese",
}

cred = credentials.Certificate("credentials.json")
# Check if the line has been executed before
if 'flag' not in st.session_state:
    # Run this block only once
    st.session_state.flag = True
    # Check if Firebase app is already initialized
    if not firebase_admin._apps:
        # Firebase app is not initialized, so initialize it
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://react-firebase-chat-fe637-default-rtdb.firebaseio.com/'
        })

# Define a simple chat storage
chat_log = []

# Translation API (MyMemory) endpoint
translation_url = "https://mymemory.translated.net/api/get"

# Streamlit app title
st.title("Chat Web with Translation")

name = st.text_input("Enter Your Name:", "Unknown")

# Create a two-column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sender")

with col2:
    st.subheader("Receiver")

# Language selection for sender
with col1:
    sender_language = st.selectbox("Select Your Language:", list(language_names.values()))

# Language selection for receiver
with col2:
    receiver_language = st.selectbox("Select Receiver's Language:", list(language_names.values()))

    if sender_language == receiver_language:
        st.warning("Sender and Receiver languages are same.")

# User message input for sender
with col1:
    user_message = st.text_area("Your Message (Sender):", "Sample", height=300)

# Additional validation for user input
if not user_message:
    st.warning("Please enter a message.")

# Additional validation for language selection
if not user_message or sender_language == receiver_language:
    st.warning("Please fill in all the required fields.")

translation = ""

with col1:
    # Translate user message for sender and display in receiver's text box
    if st.button("Send (Sender)"):
        if user_message:
            response = requests.get(
                translation_url, params={"q": user_message, "langpair": f"{sender_language}|{receiver_language}"}
            )
            translation = response.json().get("responseData", {}).get("translatedText", user_message)

            # chat_log.append({"user": user_message, "translation": translation, "sender": True})
            # # db.reference("/message").push().set(translation)
            ref = db.reference('/')

            # Set a value at a specific location
            ref.child('messages').push().set({
                'sender': name,
                'message': translation,
            })

            print(ref.get("messages"))

# Display chat log for sender in the left column
data = db.reference("/messages").get()

# Define a function to clear all messages from the database
def clear_messages():
    ref = db.reference('/messages')
    ref.delete()

# Reply to sender's message for receiver
with col2:
    # Check if messages is not empty and is a dictionary
    if isinstance(data, dict):
        # Format messages for display
        formatted_messages = "\n".join(
            [f"{message['sender']}: {message['message']}" for message_id, message in data.items()])

        # Display in a Streamlit text area
        st.text_area("Chat Pool", formatted_messages, height=300)

        # Button to clear all messages
        if st.button("Clear All Messages"):
            clear_messages()
            st.success("All messages cleared!")

    else:
        st.warning("No messages found or data is not in the expected format.")

