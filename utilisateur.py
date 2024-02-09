import mysql.connector

class Utilisateur:
    def __init__(self, nom, prenom, email):
        self.nom = nom
        self.prenom = prenom
        self.email = email

    def ajouter_utilisateur(self, db_connection, mot_de_passe):
        with db_connection.cursor() as cursor:
            try:
                query = "INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (self.nom, self.prenom, self.email, mot_de_passe))
                db_connection.commit()
                print("Utilisateur ajouté")
            except mysql.connector.errors.IntegrityError:
                print("Erreur d'intégrité : Un utilisateur avec cet email existe déjà.")

    @staticmethod
    def get_utilisateurs(db_connection):
        with db_connection.cursor() as cursor:
            query = "SELECT nom, prenom, email FROM Utilisateurs"
            cursor.execute(query)
            return [Utilisateur(nom, prenom, email) for nom, prenom, email in cursor.fetchall()]

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"







