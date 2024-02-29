import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Entry, Button
import threading
import socket
import mysql.connector

class InterfaceClient:
     
    def __init__(self, racine, email, mot_de_passe):
        self.racine = racine
        self.racine.title("Client de Chat")

        # Connexion à la base de données MySQL
        self.connexion_bd = mysql.connector.connect(
            host="ahmed-aouad.students-laplateforme.io",
            user="ahmed-aouad",
            password="ouarda2017",
            database="ahmed-aouad_mydiscord"
        )
        self.curseur_bd = self.connexion_bd.cursor()

        # Vérifier les informations d'authentification dans la base de données
        if self.verifier_authentification(email, mot_de_passe):
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

            # Connexion au serveur de chat
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect(("127.0.0.1", 55558))

            # Envoyer le pseudo au serveur
            self.socket_client.send(bytes(self.pseudo, "utf-8"))

            # Démarrer un thread pour recevoir les messages
            self.thread_reception = threading.Thread(target=self.recevoir_message)
            self.thread_reception.start()
        else:
            messagebox.showerror("Erreur d'authentification", "Email ou mot de passe incorrect. Réessayez.")

    def verifier_authentification(self, email, mot_de_passe):
        # Fonction pour vérifier les informations d'authentification dans la base de données
        query = "SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s"
        values = (email, mot_de_passe)
        self.curseur_bd.execute(query, values)
        result = self.curseur_bd.fetchone()
        return result is not None

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

    # Demander à l'utilisateur son email et mot de passe
    email = simpledialog.askstring("Authentification", "Entrez votre email:")
    mot_de_passe = simpledialog.askstring("Authentification", "Entrez votre mot de passe:")

    gui = InterfaceClient(racine, email, mot_de_passe)
    racine.mainloop()