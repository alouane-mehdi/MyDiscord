import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connexion à la base de données réussie")
        except mysql.connector.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")

    def get_connection(self):
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

