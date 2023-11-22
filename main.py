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

# ***************************************************************** working one

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
    # firebase_admin.initialize_app(cred, {
    #     'databaseURL': 'https://react-firebase-chat-fe637-default-rtdb.firebaseio.com/'
    # })




# Define a simple chat storage
chat_log = []

# Translation API (MyMemory) endpoint
translation_url = "https://mymemory.translated.net/api/get"

# Streamlit app title
st.title("Chat App with Translation")

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



# # Display chat log for sender in the left column
# with col1:
#     for chat in chat_log:
#         if chat["sender"]:
#             st.text(f"You (Sender): {chat['user']} (in {sender_language})")
#             st.text(f"Recipient: {chat['translation']} (in {receiver_language})")

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

#
# with col2:
#     # Translate user message for receiver and display in sender's text box
#     if st.button("Send (Receiver)"):
#         if user_message_receiver:
#             response = requests.get(
#                 translation_url, params={"q": user_message_receiver, "langpair": f"{receiver_language}|{sender_language}"}
#             )
#             translation = response.json().get("responseData", {}).get("translatedText", user_message_receiver)
#
#             chat_log.append({"user": user_message_receiver, "translation": translation, "sender": False})
#
# # Display chat log for receiver in the right column
# with col2:
#     for chat in chat_log:
#         if not chat["sender"]:
#             st.text(f"You (Receiver): {chat['user']} (in {receiver_language})")
#             st.text(f"Sender: {chat['translation']} (in {sender_language})")


# ***************************************************************** working testing

#
# import streamlit as st
# import requests
# import firebase_admin
# from firebase_admin import db, credentials, auth
#
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#
# # Add a nice background color
# page_bg_img = '''
# <style>
# [data-testid="stAppViewContainer"] {
#     background-image: url("https://images.unsplash.com/photo-1620121692029-d088224ddc74?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#     background-size: cover;
# }
# [data-testid="stHeader"] {
#     background-color: rgba(0, 0, 0, 0);
# }
#
# [data-testid="stToolbar"] {
#     right: 2rem;
# }
# </style>
# '''
#
# st.markdown(page_bg_img, unsafe_allow_html=True)
#
# # Mapping dictionary for language codes to names
# language_names = {
#     "en": "English",
#     "es": "Spanish",
#     "fr": "French",
#     "si": "Sinhala",
#     "ta": "Tamil",
#     "cn": "Chinese",
# }
#
# # cred = credentials.Certificate("credentials.json")
# # firebase_admin.initialize_app(cred, {
# #     'databaseURL': 'https://react-firebase-chat-fe637-default-rtdb.firebaseio.com/'
# # })
# #
# # ref = db.reference('/')
# # print( ref.get())
#
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
# # Check if the user is signed in
# user = st.experimental_get_query_params().get("user", [""])[0]
#
# if not user:
#     st.warning("You are not signed in.")
#
#     # Google Sign-In Button
#     if st.button("Sign In with Google"):
#         try:
#             # Open a new browser window to authenticate the user
#             st.markdown(
#                 "[Click here to sign in with Google](auth/signin?provider=google)",
#                 unsafe_allow_html=True,
#             )
#
#         except Exception as e:
#             st.error(f"Authentication error: {e}")
# else:
#     # The user is signed in
#     st.success(f"Welcome, {user}!")
#
#
# # Create a two-column layout
# col1, col2 = st.columns(2)
#
# with col1:
#     st.subheader("Sender")
#
# with col2:
#     st.subheader("Receiver")
#
# # Language selection for sender
# with col1:
#     sender_language = st.selectbox("Select Your Language:", list(language_names.values()))
#
# # Language selection for receiver
# with col2:
#     receiver_language = st.selectbox("Select Receiver's Language:", list(language_names.values()))
#
# # User message input for sender
# with col1:
#     user_message = st.text_area("Your Message (Sender):")
#
# translation = ""
#
# with col1:
#     # Translate user message for sender and display in receiver's text box
#     if st.button("Send (Sender)"):
#         if user_message:
#             response = requests.get(
#                 translation_url, params={"q": user_message, "langpair": f"{sender_language}|{receiver_language}"}
#             )
#             translation = response.json().get("responseData", {}).get("translatedText", user_message)
#
#             # chat_log.append({"user": user_message, "translation": translation, "sender": True})
#             db.reference("/message").push().set(translation)
#
# # Display chat log for sender in the left column
# with col1:
#     for chat in chat_log:
#         if chat["sender"]:
#             st.text(f"You (Sender): {chat['user']} (in {sender_language})")
#             st.text(f"Recipient: {chat['translation']} (in {receiver_language})")
#
# # Reply to sender's message for receiver
# with col2:
#     user_message_receiver = st.text_area("Chat Lobby:", translation)
#
# # Sign out button
# sign_out = st.button("Sign Out")
# if sign_out:
#     auth.revoke_refresh_tokens(user)
#     st.experimental_rerun()
























#
# import streamlit as st
# import requests
#
# # Mapping dictionary for language codes to names
# language_names = {
#     "en": "English",
#     "es": "Spanish",
#     "fr": "French",
#     "si": "Sinhala",
#     "ta": "Tamil",
# }
#
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#
# # Add a nice background color
# page_bg_img = '''
# <style>
# [data-testid="stAppViewContainer"] {
#     background-image: url("https://images.unsplash.com/photo-1620121692029-d088224ddc74?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#     background-size: cover;
# }
# [data-testid="stHeader"] {
#     background-color: rgba(0, 0, 0, 0);
# }
# </style>
# '''
#
# st.markdown(page_bg_img, unsafe_allow_html=True)
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
# # Create a two-column layout
# col1, col2 = st.columns(2)
#
# with col1:
#     st.subheader("Sender")
#
# with col2:
#     st.subheader("Receiver")
#
# # Language selection for sender
# with col1:
#     sender_language = st.selectbox("Select Your Language:", list(language_names.values()))
#
# # Language selection for receiver
# with col2:
#     receiver_language = st.selectbox("Select Receiver's Language:", list(language_names.values()))
#
# # User message input for sender
# with col1:
#     user_message = st.text_area("Your Message (Sender):")
#
# with col1:
#     # Translate user message for sender and display in receiver's text box
#     if st.button("Send (Sender)"):
#         if user_message:
#             response = requests.get(
#                 translation_url, params={"q": user_message, "langpair": f"{sender_language}|{receiver_language}"}
#             )
#             translation = response.json().get("responseData", {}).get("translatedText", user_message)
#
#             chat_log.append({"user": user_message, "translation": translation, "sender": True})
#
# # Display chat log for sender in the left column
# with col1:
#     for chat in chat_log:
#         if chat["sender"]:
#             st.text(f"You (Sender): {chat['user']} (in {language_names.get(sender_language)})")
#             st.text(f"Recipient: {chat['translation']} (in {language_names.get(receiver_language)})")
#
# # Reply to sender's message for receiver
# with col2:
#     user_message_receiver = st.text_area("Your Reply (Receiver):")
#
# with col2:
#     # Translate user message for receiver and display in sender's text box
#     if st.button("Send (Receiver)"):
#         if user_message_receiver:
#             response = requests.get(
#                 translation_url, params={"q": user_message_receiver, "langpair": f"{receiver_language}|{sender_language}"}
#             )
#             translation = response.json().get("responseData", {}).get("translatedText", user_message_receiver)
#
#             chat_log.append({"user": user_message_receiver, "translation": translation, "sender": False})
#
# # Display chat log for receiver in the right column
# with col2:
#     for chat in chat_log:
#         if not chat["sender"]:
#             st.text(f"You (Receiver): {chat['user']} (in {language_names.get(receiver_language)})")
#             st.text(f"Sender: {chat['translation']} (in {language_names.get(sender_language)})")


