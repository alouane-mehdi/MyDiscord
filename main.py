import sys
from PyQt5.QtWidgets import QApplication
from db import Database
from chat_application import ChatApplication 

class Main:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def connect_to_database(self):
        db = Database(self.db_host, self.db_user, self.db_password, self.db_name)
        return db.get_connection()

    def run(self):
        db_connection = self.connect_to_database()
        if db_connection is not None:
            app = QApplication(sys.argv)
            chat_application = ChatApplication(db_connection)
            chat_application.show()
            sys.exit(app.exec_())
        else:
            print("Échec de la connexion à la base de données.")

if __name__ == "__main__":
    chat_manager = Main('ahmed-aouad.students-laplateforme.io', 'ahmed-aouad', 'ouarda2017', 'ahmed-aouad_mydiscord')
    chat_manager.run()
