#main.py

import sys
from PyQt5.QtWidgets import QApplication
from db import Database
from utilisateur import Utilisateur
from canal import Canal
from chat_window import ChatWindow

def main():
    # Établir la connexion à la base de données
    db = Database('ahmed-aouad.students-laplateforme.io', 'ahmed-aouad', 'ouarda2017', 'ahmed-aouad_mydiscord')
    db_connection = db.get_connection()

    # Initialiser l'application Qt
    app = QApplication(sys.argv)

    # Vérifier si la connexion à la base de données est réussie
    if db_connection is not None:
        # Créer un nouvel utilisateur
        utilisateur = Utilisateur('Jean', 'Dupont', 'jean.dupont@email.com')
        # Ajouter l'utilisateur à la base de données avec un mot de passe
        utilisateur.ajouter_utilisateur(db_connection, 'motdepasse')

        # Créer un objet Canal pour gérer les canaux de discussion
        canal = Canal(db_connection)

        # Créer une fenêtre de chat avec l'utilisateur, le canal et la connexion à la base de données
        chat_window = ChatWindow(utilisateur, canal, db_connection)
        # Afficher la fenêtre de chat
        chat_window.show()

    # Lancer l'exécution de l'application Qt
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Appeler la fonction main pour démarrer l'application
    main()



