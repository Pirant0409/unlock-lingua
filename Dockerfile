# Utilisez une image de base
FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install libmysqlclient-dev -y
# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY main.py /app/
COPY index.html /app/
COPY utils.py /app/
COPY speech_text_speech.py /app/
COPY models.py /app/
COPY h11 /app/h11
COPY flask_sock /app/flask_sock
COPY simple_websocket /app/simple_websocket
COPY wsproto /app/wsproto
RUN mkdir -p /app/audio
RUN mkdir -p /app/audio_translated
RUN ls
# Exposez le port que votre application écoute
EXPOSE 80

# Commande pour démarrer votre application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "main:app"]
