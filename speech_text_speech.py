import os
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator

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

def translate_text(text, source_language, target_language):
    translator = Translator()

    # Split the text into chunks of 5000 characters
    chunks = [text[i:i + 5000] for i in range(0, len(text), 5000)]

    # Translate each chunk and join them
    translated_chunks = [translator.translate(chunk, src=source_language, dest=target_language).text for chunk in chunks]

    return '.'.join(translated_chunks)

def process_audio_files(audio_directory, output_directory):
    for filename in os.listdir(audio_directory):
        audio_file = os.path.join(audio_directory, filename)
        phrases = extract_phrases_from_audio(audio_file)
        text = '.'.join(phrases)  # Rejoindre toutes les phrases en une seule chaîne
        translated_text = translate_text(text, 'fr', 'en')

        # Utiliser gTTS pour générer le fichier audio à partir du texte traduit
        if translated_text.replace('.', '') == '':
            print(f"Le fichier {filename} n'a pas pu être traduit")
        else:
            tts = gTTS(translated_text, lang='en')
            output_file = os.path.join(output_directory, f"{filename.split('.')[0]}_translated.wav")
            tts.save(output_file)
        os.remove(audio_file)