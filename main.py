from flask import Flask
from flask_socketio import SocketIO
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('audio_stream')
def handle_audio_stream(audio_data):
    # Traiter les données audio ici (vous pouvez les enregistrer dans une base de données, etc.)
    print("Données audio reçues:", audio_data)  



if __name__ == '__main__':
    socketio.run(app, debug=True)
