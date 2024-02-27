import tkinter as tk
from tkinter import scrolledtext
import mysql.connector
import tempfile
import pyaudio
import wave
import pygame

# Se connecter à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alouane13011",
    database="chatdb"
)
cursor = conn.cursor()

def envoyer_message():
    sender = entry_sender.get()
    receiver = entry_receiver.get()
    message_type = "Texte" if message_mode.get() == 0 else "Audio"
    
    if message_mode.get() == 0:  # Message texte
        message = entry_message.get("1.0", tk.END).strip()
        query = "INSERT INTO messages (sender, receiver, message_type, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (sender, receiver, message_type, message))
    else:  # Message vocal
        record_audio()
        audio_path = save_audio()
        query = "INSERT INTO messages (sender, receiver, message_type, audio_path) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (sender, receiver, message_type, audio_path))

    conn.commit()
    afficher_messages()

def record_audio():
    global audio_frames
    audio_frames = []
    chunk = 1024  
    sample_format = pyaudio.paInt16  
    channels = 2
    fs = 44100  
    
    p = pyaudio.PyAudio()
    
    print('Recording...')
    
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    
    while True:
        data = stream.read(chunk)
        audio_frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def save_audio():
    filename = tempfile.mktemp(prefix="audio_", suffix=".wav", dir="")
    wf = wave.open(filename, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(audio_frames))
    wf.close()
    return filename

def afficher_messages():
    query = "SELECT sender, receiver, message_type, message, audio_path FROM messages"
    cursor.execute(query)
    messages = cursor.fetchall()
    message_box.config(state=tk.NORMAL)
    message_box.delete(1.0, tk.END)
    for sender, receiver, message_type, message, audio_path in messages:
        if message_type == "Texte":
            message_box.insert(tk.END, f"{sender} -> {receiver} (Texte): {message}\n")
        else:
            message_box.insert(tk.END, f"{sender} -> {receiver} (Audio): {audio_path}\n")
    message_box.config(state=tk.DISABLED)

# Initialiser pygame pour la lecture audio
pygame.init()

# Créer une fenêtre
root = tk.Tk()
root.title("Application de Chat")

# Créer des widgets
label_sender = tk.Label(root, text="Expéditeur:")
entry_sender = tk.Entry(root)

label_receiver = tk.Label(root, text="Destinataire:")
entry_receiver = tk.Entry(root)

label_message = tk.Label(root, text="Message:")
entry_message = scrolledtext.ScrolledText(root, width=30, height=5)

message_mode = tk.IntVar()
radio_text = tk.Radiobutton(root, text="Texte", variable=message_mode, value=0)
radio_audio = tk.Radiobutton(root, text="Audio", variable=message_mode, value=1)

button_envoyer = tk.Button(root, text="Envoyer", command=envoyer_message)
message_box = scrolledtext.ScrolledText(root, width=40, height=10, state=tk.DISABLED)

# Placer les widgets dans la fenêtre
label_sender.grid(row=0, column=0, padx=5, pady=5)
entry_sender.grid(row=0, column=1, padx=5, pady=5)

label_receiver.grid(row=1, column=0, padx=5, pady=5)
entry_receiver.grid(row=1, column=1, padx=5, pady=5)

label_message.grid(row=2, column=0, padx=5, pady=5)
entry_message.grid(row=2, column=1, padx=5, pady=5)

radio_text.grid(row=3, column=0, padx=5, pady=5)
radio_audio.grid(row=3, column=1, padx=5, pady=5)

button_envoyer.grid(row=4, column=0, columnspan=2, pady=5)

message_box.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Afficher la fenêtre
afficher_messages()
root.mainloop()

# Fermer la connexion à la base de données MySQL
cursor.close()
conn.close()
