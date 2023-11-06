import streamlit as st

# Streamlit app title
st.title("Receiver Chat App")

# Create a separate chat_log for receiver
receiver_chat_log = []

# Display receiver's chat log
for chat in receiver_chat_log:
    st.text(f"You (Receiver): {chat['user']}")
    st.text(f"Sender: {chat['translation']}")
