# Utilisez une image de base
FROM python:3.9-slim

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt /app/
COPY main.py /app/
COPY index.html /app/
COPY utils.py /app/

# Installez les dépendances
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
# Exposez le port que votre application écoute
EXPOSE 80

# Commande pour démarrer votre application
CMD ["python", "main.py"]
