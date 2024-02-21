import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog
import threading
import socket


class InterfaceClient:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Client de Chat")

        # Demander à l'utilisateur son pseudo 
        self.pseudo = simpledialog.askstring("Pseudo", "Entrez votre pseudo:")

        # Créer une zone déroulante pour le chat
        self.zone_chat = scrolledtext.ScrolledText(racine, wrap=tk.WORD, width=40, height=15)
        self.zone_chat.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Créer un widget d'entrée pour saisir les messages
        self.saisie_message = Entry(racine, width=30)
        self.saisie_message.grid(row=1, column=0, padx=10, pady=5)

        # Créer un bouton pour envoyer les messages
        self.bouton_envoi = Button(racine, text="Envoyer", command=self.envoyer_message)
        self.bouton_envoi.grid(row=1, column=1, padx=10, pady=5)

        # Créer un socket client et se connecter au serveur
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(("127.0.0.1", 55558))

  

        # Envoyer le pseudo au serveur
        self.socket_client.send(bytes(self.pseudo, "utf-8"))

        # Démarrer un thread pour recevoir les messages
        self.thread_reception = threading.Thread(target=self.recevoir_message)
        self.thread_reception.start()

      

    def envoyer_message(self):
        
        # Fonction pour envoyer un message au serveur
        message = self.saisie_message.get()
        self.socket_client.send(bytes(message, "utf-8"))
        self.saisie_message.delete(0, tk.END)

    def recevoir_message(self):

        # Fonction pour recevoir en continu et afficher les messages du serveur
        while True:
            try:
                message = self.socket_client.recv(1024).decode("utf-8")
                self.zone_chat.insert(tk.END, message + "\n")
                self.zone_chat.yview(tk.END)
            except:
                break
 
if __name__ == "__main__":
    racine = tk.Tk()
    gui = InterfaceClient(racine)
    racine.mainloop()
