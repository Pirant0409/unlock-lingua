from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from speech_text_speech import translate_text

app = Flask(__name__)

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

# Définition des routes
@app.route('/create_cours', methods=['POST'])
def create_cours():
    data = request.get_json()
    new_cours = Cours(name=data['name'], teacher=data['teacher'])
    db.session.add(new_cours)
    db.session.commit()
    return jsonify({'message': 'Cours created successfully'})

@app.route('/create_word', methods=['POST'])
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

@app.route('/get_cours', methods=['GET'])
def get_cours():
    cours = Cours.query.all()
    cours_list = []
    for c in cours:
        cours_list.append({'id': c.id, 'name': c.name, 'teacher': c.teacher})
    return jsonify({'cours': cours_list})

@app.route('/get_word', methods=['GET'])
def get_word():
    word = Word.query.all()
    word_list = []
    for w in word:
        cours = Cours.query.filter_by(id=w.cours_name).all()
        cours = cours [0]
        word_list.append({'id': w.id, 'allword': w.allword, 'date': w.date, 'heure': w.heure, 'cours_name': cours.name})
    return jsonify({'word': word_list})


@app.route('/get_translation', methods=['POST'])
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
    app.run(debug=True)