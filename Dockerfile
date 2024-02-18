# Utilisez une image de base
FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install pkg-config -y
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY h11 /app/h11
COPY flask_sock /app/flask_sock
COPY simple_websocket /app/simple_websocket
COPY wsproto /app/wsproto
COPY index.html /app/
COPY utils.py /app/
COPY speech_text_speech.py /app/
RUN mkdir -p /app/audio
RUN mkdir -p /app/audio_translated
COPY main.py /app/
# Exposez le port que votre application écoute
EXPOSE 80

# Commande pour démarrer votre application
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:80", "main:app"]
