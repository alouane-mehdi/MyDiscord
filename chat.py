import tkinter as tk
from tkinter import scrolledtext
import mysql.connector

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
    message = entry_message.get("1.0", tk.END).strip()
    query = "INSERT INTO messages (sender, receiver, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (sender, receiver, message))
    conn.commit()
    afficher_messages()

def afficher_messages():
    query = "SELECT sender, receiver, message FROM messages"
    cursor.execute(query)
    messages = cursor.fetchall()
    message_box.config(state=tk.NORMAL)
    message_box.delete(1.0, tk.END)
    for sender, receiver, message in messages:
        message_box.insert(tk.END, f"{sender} -> {receiver}: {message}\n")
    message_box.config(state=tk.DISABLED)

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

button_envoyer = tk.Button(root, text="Envoyer", command=envoyer_message)
message_box = scrolledtext.ScrolledText(root, width=40, height=10, state=tk.DISABLED)

# Placer les widgets dans la fenêtre
label_sender.grid(row=0, column=0, padx=5, pady=5)
entry_sender.grid(row=0, column=1, padx=5, pady=5)

label_receiver.grid(row=1, column=0, padx=5, pady=5)
entry_receiver.grid(row=1, column=1, padx=5, pady=5)

label_message.grid(row=2, column=0, padx=5, pady=5)
entry_message.grid(row=2, column=1, padx=5, pady=5)

button_envoyer.grid(row=3, column=0, columnspan=2, pady=5)

message_box.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Afficher la fenêtre
afficher_messages()
root.mainloop()

# Fermer la connexion à la base de données MySQL
cursor.close()
conn.close()
