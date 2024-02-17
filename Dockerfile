# Utilisez une image de base
FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg
# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app/
COPY index.html /app/
COPY utils.py /app/
COPY speech_text_speech.py /app/
COPY models /app/
COPY h11 /app/
RUN mkdir -p /app/audio
RUN mkdir -p /app/audio_translated 
COPY simple_websocket /app/
COPY wsproto /app/
COPY flask_sock /app/
# Exposez le port que votre application écoute
EXPOSE 80

# Commande pour démarrer votre application
CMD ["python", "main.py"]
