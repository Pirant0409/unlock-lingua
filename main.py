from flask import Flask, render_template,jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from flask_sock import Sock
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from speech_text_speech import translate_text
import base64
import os
from utils import hexToMp3

app = Flask(__name__)
CORS(app)
sock = Sock(app)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u602119779_antoi:*1udazPbC@sql713.main-hosting.eu:3306/u602119779_lesmarostin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

# Définition des modèles de base de données
class Cours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allword = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    heure = db.Column(db.String(100), nullable=False)
    cours_name = db.Column(db.Integer, db.ForeignKey('cours.name'), nullable=False)

@app.route('/api/')
def index():
    return render_template('./index.html')

@sock.route('/api/audio_stream')
 #@cross-origin()
def audio_stream(ws):
    try:
        audio_data = ws.receive()
        print("-----Données audio reçues-----\n")
        print(audio_data)
        print("\n-----Données audio envoyées-----\n")
        # Traiter les données audio ici (vous pouvez les enregistrer dans une base de données, etc.)
        hexToMp3(audio_data)
    except Exception as e:
        print("Erreur lors du traitement des données audio:", str(e))

@app.route('/api/get_file_names', methods=['GET'])
def get_file_names():
    file_names = []
    for filename in os.listdir("./audio_translated"):
        file_names.append(filename)
    response = jsonify({'file_names': file_names})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/get_audio/<path:filename>')
def get_audio(filename):
    return send_from_directory('audio_translated', filename)

@app.route('/api/del_audio/<path:filename>', methods=['DELETE'])
@cross_origin()
def del_audio(filename):
    if os.path.exists(f"./audio_translated/{filename}"):
        os.remove(f"./audio_translated/{filename}")
        return jsonify({'message': 'Audio deleted successfully'})
    else:
        return jsonify({'error': 'Audio not found'})
# Définition des routes
@app.route('/api/create_cours', methods=['POST'])
@cross_origin()
def create_cours():
    data = request.get_json()
    new_cours = Cours(name=data['name'], teacher=data['teacher'])
    db.session.add(new_cours)
    db.session.commit()
    return jsonify({'message': 'Cours created successfully'})

@app.route('/api/create_word', methods=['POST'])
@cross_origin()
def create_word():
    data = request.get_json()
    cours = Cours.query.filter_by(id=data['cours_name']).first()
    if not cours:
        return jsonify({'error': 'Cours not found'}), 404
        # Récupérer la date et l'heure actuelles
    current_datetime = datetime.now()

    # Convertir la date en format string (YYYY-MM-DD)
    date_string = current_datetime.strftime('%Y-%m-%d')

    # Convertir l'heure en format string (HH:MM:SS)
    heure_string = current_datetime.strftime('%H:%M')

    new_word = Word(allword=data['allword'], date=date_string, heure=heure_string, cours_name=data['cours_name'])
    db.session.add(new_word)
    db.session.commit()
    return jsonify({'message': 'Word created successfully'})

@app.route('/api/get_cours', methods=['GET'])
def get_cours():
    cours = Cours.query.all()
    cours_list = []
    for c in cours:
        cours_list.append({'id': c.id, 'name': c.name, 'teacher': c.teacher})
    response = jsonify({'cours': cours_list})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/get_word', methods=['GET'])
@cross_origin(origin='*')
def get_word():
    word = Word.query.all()
    word_list = []
    for w in word:
        cours = Cours.query.filter_by(id=w.cours_name).all()
        cours = cours [0]
        word_list.append({'id': w.id, 'allword': w.allword, 'date': w.date, 'heure': w.heure, 'cours_name': cours.name})
    response = jsonify({'word': word_list})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/get_translation', methods=['POST'])
@cross_origin()
def get_translation():
    # Récupérer les données JSON envoyées dans la requête
    data = request.get_json()

    # Extraire les mots à traduire et la langue cible depuis les données JSON
    words = data.get('words')  # Récupérer les mots, ou une chaîne vide si non spécifié
    language = data.get('language')  # Récupérer la langue cible, ou 'fr' par défaut

    # Utiliser une fonction de traduction pour traduire les mots
    translated_words = translate_text(words, "fr", language)

    # Renvoyer la traduction sous forme de JSON
    return jsonify({'translated_words': translated_words})


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)
