# utilisateur.py

import mysql.connector

class Utilisateur:
    def __init__(self, nom, prenom, email):
        self.nom = nom
        self.prenom = prenom
        self.email = email

    def ajouter_utilisateur(self, db_connection, mot_de_passe):
        # Méthode pour ajouter un utilisateur à la base de données
        with db_connection.cursor() as cursor:
            try:
                # Query pour insérer un nouvel utilisateur dans la table Utilisateurs
                query = "INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
                # Exécution de la query avec les valeurs fournies
                cursor.execute(query, (self.nom, self.prenom, self.email, mot_de_passe))
                # Validation de la transaction
                db_connection.commit()
                print("Utilisateur ajouté")
            except mysql.connector.errors.IntegrityError:
                # Gestion de l'erreur en cas de violation de contrainte d'intégrité (email déjà existant)
                print("Erreur d'intégrité : Un utilisateur avec cet email existe déjà.")

    @staticmethod
    def get_utilisateurs(db_connection):
        # Méthode statique pour récupérer tous les utilisateurs depuis la base de données
        with db_connection.cursor() as cursor:
            # Query pour sélectionner tous les utilisateurs de la table Utilisateurs
            query = "SELECT nom, prenom, email FROM Utilisateurs"
            # Exécution de la query
            cursor.execute(query)
            # Création d'une liste d'instances Utilisateur à partir des résultats
            return [Utilisateur(nom, prenom, email) for nom, prenom, email in cursor.fetchall()]

    @property
    def nom_complet(self):
        # Propriété pour obtenir le nom complet de l'utilisateur
        return f"{self.prenom} {self.nom}"








