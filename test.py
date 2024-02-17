import pyttsx3

def save_text_to_audio_file(text, output_file):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()

text_to_convert1 = "Hello, notre projet consiste en de la traduction en live. L'idée est qu'il faut aider les primo arrivant à comprendre le français. "
text_to_convert2 = "En plus, il aurait moyen de garder des listes de mot. ça leur permet d'apprendre les mot important du cours "
text_to_convert3 = "Etre ou ne pas être, telle est la question. Est-ce à l'âme plus de noblesse que de la fortune les outrages endurer, plutôt que de prendre les armes contre une mer de souffrance, de combattre et de les achever ? Mourir, dormir, rien de plus."
output_file2 = "output_audio_2.mp3"
output_file1 = "output_audio_1.mp3"
output_file3 = "output_audio_3.mp3"

save_text_to_audio_file(text_to_convert1, output_file1)
print(f"Audio saved to {output_file1}")

save_text_to_audio_file(text_to_convert2, output_file2)
print(f"Audio saved to {output_file2}")

save_text_to_audio_file(text_to_convert3, output_file3)
print(f"Audio saved to {output_file3}")

