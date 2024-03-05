import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QMessageBox, QMenu, QAction
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
        self.clearLayout(self.layout_principal)

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
        self.emoticone_btn = QPushButton('😀')

        self.layout_principal.addWidget(self.zone_messages)
        self.layout_principal.addWidget(self.message_edit)
        self.layout_principal.addWidget(self.envoyer_btn)
        self.layout_principal.addWidget(self.deconnexion_btn)
        self.layout_principal.addWidget(self.emoticone_btn)

        self.envoyer_btn.clicked.connect(self.envoyerMessage)
        self.deconnexion_btn.clicked.connect(self.deconnexion)
        self.emoticone_btn.clicked.connect(self.ouvrirMenuEmoticones)
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
            with self.db_connection.cursor(buffered=True) as cursor:
                try:
                    query = "INSERT INTO Utilisateurs (email, mot_de_passe, prenom, nom) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (email, mdp, prenom, nom))
                    self.db_connection.commit()
                    QMessageBox.information(self, 'Succès', 'Utilisateur enregistré avec succès!')
                    self.estConnecte = True
                    self.user_email = email
                    self.prenom = prenom
                    self.setupChatUI()
                except mysql.connector.Error as e:
                    self.db_connection.rollback()
                    QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'enregistrement: {e}')
        else:
            QMessageBox.critical(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def verifier_connexion(self, email, mot_de_passe):
        with self.db_connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT mot_de_passe FROM Utilisateurs WHERE email = %s", (email,))
            result = cursor.fetchone()
            return result and result[0] == mot_de_passe

    def envoyerMessage(self):
        if self.estConnecte:
            message = self.message_edit.text().strip()
            if message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                formatted_message = f"[{timestamp}] {self.prenom}: {message}"
                self.zone_messages.append(formatted_message)
                self.enregistrerMessage(message)
                self.message_edit.clear()

    def enregistrerMessage(self, message):
        with self.db_connection.cursor(buffered=True) as cursor:
            query = "INSERT INTO Messages (id_utilisateur, contenu, date_publication) VALUES ((SELECT id_utilisateur FROM Utilisateurs WHERE email = %s), %s, NOW())"
            cursor.execute(query, (self.user_email, message))
            self.db_connection.commit()

    def chargerHistorique(self):
        with self.db_connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT contenu, date_publication FROM Messages WHERE id_utilisateur = (SELECT id_utilisateur FROM Utilisateurs WHERE email = %s) ORDER BY date_publication ASC", (self.user_email,))
            for (contenu, date_publication) in cursor:
                if date_publication:
                    timestamp = date_publication.strftime('%Y-%m-%d %H:%M:%S')
                    formatted_message = f"[{timestamp}] {self.prenom}: {contenu}"
                else:
                    formatted_message = "[Date inconnue] {self.prenom}: {contenu}"
                self.zone_messages.append(formatted_message)

    def deconnexion(self):
        self.estConnecte = False
        self.user_email = ''
        self.prenom = ''  # Réinitialiser le prénom lors de la déconnexion
        self.setupConnexionUI()

    def recuperer_prenom(self, email):
        with self.db_connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT prenom FROM Utilisateurs WHERE email = %s", (email,))
            result = cursor.fetchone()
            return result[0] if result else "Inconnu"

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
            QLineEdit, QTextEdit, QPushButton {
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

    def ouvrirMenuEmoticones(self):
        menu_emoticones = QMenu(self)
        emoticones = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚']
        for emo in emoticones:
            action = QAction(emo, self)
            action.triggered.connect(lambda checked, e=emo: self.message_edit.insert(e))
            menu_emoticones.addAction(action)
        menu_emoticones.exec_(self.emoticone_btn.mapToGlobal(self.emoticone_btn.rect().bottomLeft()))

def main():
    db_connection = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )

    app = QApplication(sys.argv)
    chat_application = ChatApplication(db_connection)
    chat_application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
