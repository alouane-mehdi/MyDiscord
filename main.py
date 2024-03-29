#main.py

import sys
from PyQt5.QtWidgets import QApplication
from db import Database
from utilisateur import Utilisateur
from canal import Canal
from chat_window import ChatWindow

def main():
    db = Database('ahmed', 'root', 'ouarda2017', 'myDiscord')
    db_connection = db.get_connection()

    app = QApplication(sys.argv)

    if db_connection is not None:
        utilisateur = Utilisateur('Jean', 'Dupont', 'jean.dupont@email.com')
        utilisateur.ajouter_utilisateur(db_connection, 'motdepasse')

        canal = Canal(db_connection)

        chat_window = ChatWindow(utilisateur, canal, db_connection)  # Passez db_connection ici
        chat_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



