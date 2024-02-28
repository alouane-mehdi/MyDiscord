import sys
from PyQt5.QtWidgets import QApplication
from db import Database
from chat_window import ChatWindow

def main():
    
    db = Database('ahmed-aouad.students-laplateforme.io', 'ahmed-aouad', 'ouarda2017', 'ahmed-aouad_mydiscord')
    db_connection = db.get_connection()

    app = QApplication(sys.argv)

    if db_connection is not None:
        chat_window = ChatWindow(db_connection)
        chat_window.show()
    else:
        print("Échec de la connexion à la base de données.")

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
