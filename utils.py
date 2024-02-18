import numpy as np
import base64
import os
import speech_text_speech as stt
from io import BytesIO
from pydub import AudioSegment

def hexToMp3(audioString,i):

    newAudioString = base64.b64decode(audioString)
    print("Decodage de l'audio")
    audio_bytes_io = BytesIO(newAudioString)
    print("Conversion de l'audio en mp3")
    audio = AudioSegment.from_file(audio_bytes_io)
    if os.listdir("./audio") == []:
        i = 0
    else:
        files_list = os.listdir("./audio")
        i = int(files_list[-1].split("_")[0]) + 1
    audio.export("./audio/"+str(i)+"_output.wav", format="wav")
    print("Audio créé avec succès")
    stt.process_audio_files("./audio", "./audio_translated")
    print("Audio traité avec succès")