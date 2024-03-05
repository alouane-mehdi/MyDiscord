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

    def get_channels(self):
        channels = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id_canal, nom_canal FROM Canaux")
            channels = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération des canaux: {e}")
        return channels

    def get_channel_messages(self, channel_id):
        messages = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT contenu, date_publication FROM Messages WHERE id_canal = %s", (channel_id,))
            messages = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération des messages du canal: {e}")
        return messages

    def add_message(self, channel_id, content):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Messages (id_canal, contenu) VALUES (%s, %s)", (channel_id, content))
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as e:
            print(f"Erreur lors de l'ajout du message: {e}")
