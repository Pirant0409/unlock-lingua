from flask import Flask, render_template
from flask_cors import CORS
from flask_sock import Sock
import base64
from utils import hexToMp3

app = Flask(__name__)
CORS(app)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/audio_stream')
 #@cross-origin()
def audio_stream(ws):
    while True:
        audio_data = ws.receive()
        print("-----Données audio reçues-----\n")
        ws.send(audio_data)
        print(audio_data)
        print("\n-----Données audio envoyées-----\n")
        # Traiter les données audio ici (vous pouvez les enregistrer dans une base de données, etc.)
        hexToMp3(audio_data)

@app.route('/proxy_api')
def proxy_api():
    return "Hello from the proxy API!"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)
