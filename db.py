# db.py

import mysql.connector  # Importation du module pour la connexion MySQL

class Database:
    def __init__(self, host, user, password, database):
        try:
            # Tentative de connexion à la base de données avec les paramètres fournis
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            # Si la connexion réussit, afficher un message de confirmation
            print("Connexion à la base de données réussie")
        except mysql.connector.Error as e:
            # En cas d'erreur lors de la connexion, afficher un message d'erreur
            print(f"Erreur de connexion à la base de données: {e}")
            self.connection = None  # Définir la connexion à None en cas d'échec

    def get_connection(self):
        # Fonction pour obtenir la connexion à la base de données
        return self.connection  # Retourne l'objet de connexion


