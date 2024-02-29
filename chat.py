import tkinter as tk
from tkinter import scrolledtext, filedialog
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat Textuel avec Messages Vocaux")

        self.message_area = scrolledtext.ScrolledText(master, state='disabled')
        self.message_area.pack(expand=True, fill='both')

        self.entry = tk.Entry(master)
        self.entry.pack(expand=True, fill='x')
        self.entry.bind("<Return>", self.send_message)

        self.record_button = tk.Button(master, text="Enregistrer Message Vocal", command=self.record_audio)
        self.record_button.pack(expand=True, fill='x')

        self.messages = []  # Pour stocker les messages vocaux

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.message_area.configure(state='normal')
            self.message_area.insert('end', f"Me: {message}\n")
            self.message_area.configure(state='disabled')
            self.entry.delete(0, 'end')

    def record_audio(self):
        duration = 5  # Durée de l'enregistrement en secondes

        # Enregistrement audio depuis le microphone
        audio_data = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype='int16')
        sd.wait()

        # Chemin d'accès pour sauvegarder le fichier audio
        audio_file = "message_audio.wav"

        # Enregistrement des données audio dans un fichier WAV
        sf.write(audio_file, audio_data, 44100, 'PCM_24')

        # Ajouter le fichier audio à la liste des messages vocaux
        self.messages.append(audio_file)

        # Afficher le message vocal dans la fenêtre de chat
        self.display_audio_message(audio_file)

    def display_audio_message(self, audio_file):
        play_button = tk.Button(self.master, text="Lire", command=lambda: self.play_audio(audio_file))
        self.message_area.window_create('end', window=play_button)
        self.message_area.insert('end', '\n')

    def play_audio(self, audio_file):
        audio = AudioSegment.from_file(audio_file)
        play(audio)

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
