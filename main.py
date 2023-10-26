import streamlit as st
import requests
from threading import Thread
import time

# Define a simple chat storage
chat_log = []

# Translation API (MyMemory) endpoint
translation_url = "https://mymemory.translated.net/api/get"

# Streamlit app title
st.title("Chat App with Translation")

# Language selection
recipient_language = st.selectbox("Select Your Language:", ["en", "es", "fr"])

# User message input
user_message = st.text_area("Your Message:")

# Translate user message
if st.button("Send"):
    if user_message:
        response = requests.get(
            translation_url, params={"q": user_message, "langpair": f"en|{recipient_language}"}
        )
        translation = response.json().get("responseData", {}).get("translatedText", user_message)

        chat_log.append({"user": user_message, "translation": translation})

# Display chat log
for chat in chat_log:
    st.text(f"You: {chat['user']}")
    st.text(f"Recipient: {chat['translation']}")


# Simulate real-time chat between two users on the same localhost
def chat_simulator():
    while True:
        if len(chat_log) > 1:
            time.sleep(2)
            if chat_log[-2]["user"] == chat_log[-1]["user"]:
                chat_log.pop(-1)
        st.text("")

# Start the chat simulator in a separate thread
Thread(target=chat_simulator).start()
