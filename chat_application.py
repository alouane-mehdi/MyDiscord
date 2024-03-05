import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QMessageBox
from datetime import datetime
import mysql.connector

class ChatApplication(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.estConnecte = False
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout(self.central_widget)
        self.setupConnexionUI()

        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle('Connexion - Chat')
        self.appliquerStyles()

    def setupConnexionUI(self):
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")
        self.mdp_edit = QLineEdit()
        self.mdp_edit.setPlaceholderText("Mot de passe")
        self.mdp_edit.setEchoMode(QLineEdit.Password)
        self.prenom_edit = QLineEdit()
        self.prenom_edit.setPlaceholderText("Prénom")
        self.nom_edit = QLineEdit()
        self.nom_edit.setPlaceholderText("Nom")
        self.connexion_btn = QPushButton('Connexion')
        self.enregistrement_btn = QPushButton('Enregistrement')

        self.layout_principal.addWidget(QLabel('Email'))
        self.layout_principal.addWidget(self.email_edit)
        self.layout_principal.addWidget(QLabel('Mot de passe'))
        self.layout_principal.addWidget(self.mdp_edit)
        self.layout_principal.addWidget(QLabel('Prénom'))
        self.layout_principal.addWidget(self.prenom_edit)
        self.layout_principal.addWidget(QLabel('Nom'))
        self.layout_principal.addWidget(self.nom_edit)
        self.layout_principal.addWidget(self.connexion_btn)
        self.layout_principal.addWidget(self.enregistrement_btn)

        self.connexion_btn.clicked.connect(self.connecterUtilisateur)
        self.enregistrement_btn.clicked.connect(self.enregistrerUtilisateur)

    def setupChatUI(self):
        self.clearLayout(self.layout_principal)
        self.zone_messages = QTextEdit()
        self.zone_messages.setReadOnly(True)
        self.message_edit = QLineEdit()
        self.message_edit.setPlaceholderText("Écrivez votre message ici...")
        self.envoyer_btn = QPushButton('Envoyer')
        self.deconnexion_btn = QPushButton('Déconnexion')

        self.layout_principal.addWidget(self.zone_messages)
        self.layout_principal.addWidget(self.message_edit)
        self.layout_principal.addWidget(self.envoyer_btn)
        self.layout_principal.addWidget(self.deconnexion_btn)

        self.envoyer_btn.clicked.connect(self.envoyerMessage)
        self.deconnexion_btn.clicked.connect(self.deconnexion)

        self.chargerHistorique()

    def connecterUtilisateur(self):
        email = self.email_edit.text().strip()
        mdp = self.mdp_edit.text().strip()
        if self.verifier_connexion(email, mdp):
            self.estConnecte = True
            self.user_email = email
            self.prenom = self.recuperer_prenom(email)
            self.setupChatUI()
        else:
            QMessageBox.critical(self, 'Erreur', 'Email ou mot de passe incorrect.')

    def enregistrerUtilisateur(self):
        email = self.email_edit.text().strip()
        mdp = self.mdp_edit.text().strip()
        prenom = self.prenom_edit.text().strip()
        nom = self.nom_edit.text().strip()

        if email and mdp and prenom and nom:
            with self.db_connection.cursor() as cursor:
                try:
                    query = "INSERT INTO Utilisateurs (email, mot_de_passe, prenom, nom) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (email, mdp, prenom, nom))
                    self.db_connection.commit()
                    QMessageBox.information(self, 'Succès', 'Utilisateur enregistré avec succès!')
                    self.connecterUtilisateur()
                except Exception as e:
                    self.db_connection.rollback()
                    QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'enregistrement: {e}')
        else:
            QMessageBox.critical(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def envoyerMessage(self):
        message = self.message_edit.text().strip()
        if message:
            self.enregistrerMessage(message)
            self.afficherMessage(message, self.prenom)
            self.message_edit.clear()

    def afficherMessage(self, message, prenom):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] {prenom}: {message}"
        self.zone_messages.append(formatted_message)

    def enregistrerMessage(self, message):
        id_utilisateur = self.recupererIdUtilisateur()
        if id_utilisateur is not None:
            with self.db_connection.cursor() as cursor:
                try:
                    query = "INSERT INTO Messages (id_utilisateur, contenu, date_publication) VALUES (%s, %s, NOW())"
                    cursor.execute(query, (id_utilisateur, message))
                    self.db_connection.commit()
                except Exception as e:
                    self.db_connection.rollback()
                    print(f"Erreur lors de l'enregistrement du message: {e}")

    def chargerHistorique(self):
        id_utilisateur = self.recupererIdUtilisateur()
        if id_utilisateur is not None:
            with self.db_connection.cursor() as cursor:
                try:
                    query = "SELECT contenu, date_publication FROM Messages WHERE id_utilisateur = %s ORDER BY date_publication ASC"
                    cursor.execute(query, (id_utilisateur,))
                    for contenu, date_publication in cursor:
                        self.afficherMessage(contenu, "Historique")
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'historique: {e}")

    def deconnexion(self):
        self.estConnecte = False
        self.user_email = ''
        self.prenom = ''
        self.clearLayout(self.layout_principal)
        self.setupConnexionUI()

    def verifier_connexion(self, email, mot_de_passe):
        with self.db_connection.cursor() as cursor:
            query = "SELECT * FROM Utilisateurs WHERE email=%s AND mot_de_passe=%s"
            cursor.execute(query, (email, mot_de_passe))
            result = cursor.fetchone()
            return True if result else False

    def recuperer_prenom(self, email):
        with self.db_connection.cursor() as cursor:
            query = "SELECT prenom FROM Utilisateurs WHERE email=%s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result[0] if result else None

    def recupererIdUtilisateur(self):
        with self.db_connection.cursor() as cursor:
            query = "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s"  # Ajusté pour utiliser id_utilisateur
            cursor.execute(query, (self.user_email,))
            result = cursor.fetchone()
            return result[0] if result else None

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def appliquerStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #36393f;
            }
            QLineEdit, QTextEdit {
                background-color: #40444b;
                color: #ffffff;
                border: None;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #7289da;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
                border: None;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
        """)

def main():
    db_connection = mysql.connector.connect(
        host='ahmed-aouad.students-laplateforme.io',
        user='ahmed-aouad',
        password='ouarda2017',
        database='ahmed-aouad_mydiscord'
    )

    app = QApplication(sys.argv)
    chat_application = ChatApplication(db_connection)
    chat_application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
