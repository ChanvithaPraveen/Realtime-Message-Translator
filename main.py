# import streamlit as st
# import requests
# from threading import Thread
# import time
#
# # Define a simple chat storage
# chat_log = []
#
# # Translation API (MyMemory) endpoint
# translation_url = "https://mymemory.translated.net/api/get"
#
# # Streamlit app title
# st.title("Chat App with Translation")
#
# # Language selection
# recipient_language = st.selectbox("Select Your Language:", ["en", "es", "fr"])
#
# # User message input
# user_message = st.text_area("Your Message:")
#
# # Translate user message
# if st.button("Send"):
#     if user_message:
#         response = requests.get(
#             translation_url, params={"q": user_message, "langpair": f"en|{recipient_language}"}
#         )
#         translation = response.json().get("responseData", {}).get("translatedText", user_message)
#
#         chat_log.append({"user": user_message, "translation": translation})
#
# # Display chat log
# for chat in chat_log:
#     st.text(f"You: {chat['user']}")
#     st.text(f"Recipient: {chat['translation']}")
#
#
# # Simulate real-time chat between two users on the same localhost
# def chat_simulator():
#     while True:
#         if len(chat_log) > 1:
#             time.sleep(2)
#             if chat_log[-2]["user"] == chat_log[-1]["user"]:
#                 chat_log.pop(-1)
#         st.text("")
#
# # Start the chat simulator in a separate thread
# Thread(target=chat_simulator).start()



import streamlit as st
import requests

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Define a simple chat storage
chat_log = []

# Translation API (MyMemory) endpoint
translation_url = "https://mymemory.translated.net/api/get"

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
    sender_language = st.selectbox("Select Your Language:", ["en", "es", "fr"])

# Language selection for receiver
with col2:
    receiver_language = st.selectbox("Select Receiver's Language:", ["en", "es", "fr"])

# User message input for sender
with col1:
    user_message = st.text_area("Your Message (Sender):")

with col1:
    # Translate user message for sender and display in receiver's text box
    if st.button("Send (Sender)"):
        if user_message:
            response = requests.get(
                translation_url, params={"q": user_message, "langpair": f"{sender_language}|{receiver_language}"}
            )
            translation = response.json().get("responseData", {}).get("translatedText", user_message)

            chat_log.append({"user": user_message, "translation": translation, "sender": True})

# Display chat log for sender in the left column
with col1:
    for chat in chat_log:
        if chat["sender"]:
            st.text(f"You (Sender): {chat['user']} (in {sender_language})")
            st.text(f"Recipient: {chat['translation']} (in {receiver_language})")

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

            chat_log.append({"user": user_message_receiver, "translation": translation, "sender": False})

# Display chat log for receiver in the right column
with col2:
    for chat in chat_log:
        if not chat["sender"]:
            st.text(f"You (Receiver): {chat['user']} (in {receiver_language})")
            st.text(f"Sender: {chat['translation']} (in {sender_language})")



