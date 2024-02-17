import numpy as np
import base64
import os
import speech_text_speech as stt
from io import BytesIO
from pydub import AudioSegment

def hexToMp3(audioString):

    newAudioString = base64.b64decode(audioString)
    print("Decodage de l'audio")
    audio_bytes_io = BytesIO(newAudioString)
    print("Conversion de l'audio en mp3")
    audio = AudioSegment.from_file(audio_bytes_io)
    if os.path.exists("./audio/output.wav"):
        os.remove("./audio/output.wav")
    audio.export("./audio/output.wav", format="wav")
    print("Audio créé avec succès")
    stt.process_audio_files("./audio", "./audio_translated")
    print("Audio traité avec succès")