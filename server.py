import requests
import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Initialize message variables
sender_message = ""
sender_translation = ""

# Event handler for receiving messages from the sender
@sio.on('sender_message')
def handle_message(sid, message):
    # Translate the message and send it to the receiver
    response = requests.get(
        "https://mymemory.translated.net/api/get",
        params={"q": message, "langpair": "en|es"}  # Translate from English to Spanish
    )
    translation = response.json().get("responseData", {}).get("translatedText", message)

    sio.emit('message_from_sender', {'message': message, 'translation': translation})

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5001)), app)
