import mysql.connector

class Utilisateur:
    def __init__(self, email, prenom=None, nom=None):
        self.email = email
        self.prenom = prenom
        self.nom = nom

    def ajouter_utilisateur(self, db_connection, mot_de_passe):
        with db_connection.cursor() as cursor:
            try:
                query = "INSERT INTO Utilisateurs (email, mot_de_passe, prenom, nom) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (self.email, mot_de_passe, self.prenom, self.nom))
                db_connection.commit()
            except mysql.connector.Error as e:
                print(f"Erreur lors de l'ajout de l'utilisateur: {e}")

    @staticmethod
    def verifier_connexion(db_connection, email, mot_de_passe):
        with db_connection.cursor() as cursor:
            query = "SELECT * FROM Utilisateurs WHERE email=%s AND mot_de_passe=%s"
            cursor.execute(query, (email, mot_de_passe))
            result = cursor.fetchone()
            return True if result else False
