<h1 align="center">
  <br>
   Chat Web with Translation
  <br>
</h1>

<h4 align="center">This repository contains the source code for a simple chat web application with translation functionality. Users can input messages in their preferred language, which are then translated and displayed in the recipient's chosen language.

<p align="center">
  <a href="https://"><img src="https://img.shields.io/badge/language-Python-2ea42f?logo=python" alt="language - Python"></a>
  <a href="https://"><img src="https://img.shields.io/badge/framework-Streamlit-2ea42f?logo=streamlit" alt="language - Stramlit"></a>
  <a href="https://"><img src="https://img.shields.io/badge/Python Streamlit application-localhost-orange?logo=IDE" alt="Python-Streamlit-application"></a>
  <br>
</p>

# Description

## Technologies Used

- Streamlit: For building the web application interface.
- Firebase Realtime Database: For storing and retrieving chat messages.
- MyMemory Translation API: For translating messages between different languages.

## Features

- Users can input messages in their preferred language.
- Messages are translated into the recipient's chosen language.
- Support for multiple languages, including English, Spanish, French, Sinhala, Tamil, and Chinese.

## Setup Instructions

1. Clone the repository: `git clone <repository_url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a Firebase project and set up a Realtime Database.
4. Obtain the credentials for accessing the Firebase Realtime Database and save them in a `credentials.json` file.
5. Set the Firebase Realtime Database URL as an environment variable named `FIREBASE_DATABASE_URL`.
6. Run the Streamlit app: `streamlit run app.py`

## Usage

1. Access the Streamlit app through the provided URL.
2. Enter your name and select your preferred language.
3. Choose the recipient's language.
4. Type your message in the sender's text box and click "Send (Sender)".
5. View the translated message in the receiver's text box.

![Input_not_Colorized_Image](Translator.png)
