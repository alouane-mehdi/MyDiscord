import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Connexion à la base de données réussie")
        except mysql.connector.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            self.connection = None

    def get_connection(self):
        return self.connection


