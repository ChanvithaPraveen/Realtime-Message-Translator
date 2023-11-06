import socket
import threading

import streamlit as st
from googletrans import Translator

# Define the server host and port
HOST = '127.0.0.1'
PORT = 8504

# Create a socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            st.write(message)
        except:
            st.error("An error occurred!")
            client.close()
            break

# Function to send messages to the server
def send(message):
    if message.lower() == 'exit':
        client.send('exit'.encode('utf-8'))
        client.close()
    else:
        client.send(message.encode('utf-8'))

# Create a Streamlit app
st.title("Real-Time Chat Application")

# Text input to send messages
message = st.text_input("Type your message:")
if st.button("Send"):
    send(message)

# Create a Streamlit thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()
