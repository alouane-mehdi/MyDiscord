import sys
from PyQt5.QtWidgets import QApplication
from db import Database
from chat_application import ChatApplication  

def main():
    # Initialisation de la connexion à la base de données
    db = Database('ahmed-aouad.students-laplateforme.io', 'ahmed-aouad', 'ouarda2017', 'ahmed-aouad_mydiscord')
    db_connection = db.get_connection()

    # Initialisation de l'application Qt
    app = QApplication(sys.argv)

    if db_connection is not None:
        # Création et affichage de la fenêtre principale de l'application de chat
        chat_application = ChatApplication(db_connection)
        chat_application.show()
    else:
        print("Échec de la connexion à la base de données.")

    # Exécution de l'application Qt et sortie propre à la fermeture
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


    # test historique avec cristiano et abdel 