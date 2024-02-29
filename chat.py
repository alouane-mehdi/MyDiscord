import tkinter as tk
from tkinter import scrolledtext, filedialog
import pygame
import os
import sounddevice as sd
from scipy.io.wavfile import write

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

        self.play_button = tk.Button(master, text="Lire Message Vocal", command=self.select_audio_file)
        self.play_button.pack(expand=True, fill='x')

        self.setup_audio()

    def setup_audio(self):
        pygame.mixer.init()

    def send_message(self, event=None):
        message = self.entry.get()
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
        write(audio_file, 44100, audio_data)

        # Lecture du fichier audio enregistré
        self.play_audio(audio_file)

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.wav")])
        if file_path:
            self.play_audio(file_path)

    def play_audio(self, audio_file):
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Erreur de lecture audio : {e}")

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
