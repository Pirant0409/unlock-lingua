import numpy as np
import base64
from io import BytesIO
from pydub import AudioSegment
def hexToMp3(audioString):

    newAudioString = base64.b64decode(audioString)
    print("Decodage de l'audio")
    audio_bytes_io = BytesIO(newAudioString)
    print("Conversion de l'audio en mp3")
    audio = AudioSegment.from_file(audio_bytes_io)
    audio.export("./audio/output.mp3", format="mp3")
    print("Audio créé avec succès")