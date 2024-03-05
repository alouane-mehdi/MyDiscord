# canal.py

import mysql.connector

class Canal:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def creer_canal(self, nom_canal, est_prive):
        with self.db_connection.cursor() as cursor:
            try:
                query = "INSERT INTO Canaux (nom_canal, est_prive) VALUES (%s, %s)"
                cursor.execute(query, (nom_canal, est_prive))
                self.db_connection.commit()
                print("Canal créé")
            except mysql.connector.Error as e:
                print(f"Erreur lors de la création du canal: {e}")

    def get_canaux(self):
        with self.db_connection.cursor() as cursor:
            query = "SELECT nom_canal FROM Canaux"
            cursor.execute(query)
            return cursor.fetchall()



