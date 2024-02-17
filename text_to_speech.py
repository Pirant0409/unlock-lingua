import os
import speech_recognition as sr
import pyttsx3

def extract_phrases_from_audio(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Enregistre l'audio du fichier

    try:
        # Utilise la reconnaissance vocale pour transcrire l'audio en texte
        text = recognizer.recognize_google(audio_data, language="fr-FR")
        phrases = text.split('.')  # Sépare le texte en phrases
        return phrases
    except sr.UnknownValueError:
        print("Impossible de reconnaître l'audio")
        return []
    except sr.RequestError as e:
        print(f"Erreur lors de la requête à l'API de reconnaissance vocale : {e}")
        return []

def save_text_to_audio_file(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()


def process_audio_files(audio_directory):
    for filename in os.listdir(audio_directory):
        audio_file = os.path.join(audio_directory, filename)
        phrases = extract_phrases_from_audio(audio_file)
        save_text_to_audio_file(phrases)

audio_directory = "C:/Users/theol/Documents/Unamur/Master2/Hackaton/audio"
process_audio_files(audio_directory)
