import streamlit as st
import requests

# Define a simple chat storage
chat_log = []

# Translation API (MyMemory) endpoint
translation_url = "https://mymemory.translated.net/api/get"

# Streamlit app title
st.title("Sender Chat App")

# Language selection for sender
sender_language = st.selectbox("Select Your Language:", ["en", "es", "fr"])

# User message input for sender
user_message = st.text_area("Your Message:")

# Translate user message for sender
if st.button("Send"):
    if user_message:
        response = requests.get(
            translation_url, params={"q": user_message, "langpair": f"en|{sender_language}"}
        )
        translation = response.json().get("responseData", {}).get("translatedText", user_message)

        chat_log.append({"user": user_message, "translation": translation})

# Display sender's chat log
for chat in chat_log:
    st.text(f"You (Sender): {chat['user']}")
    st.text(f"Recipient: {chat['translation']}")
