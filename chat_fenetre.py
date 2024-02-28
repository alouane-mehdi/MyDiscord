from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from datetime import datetime

class ChatFenetre(QWidget):
    def __init__(self, prenom='', db_connection=None, user_email=''):
        super().__init__()
        self.prenom = prenom
        self.db_connection = db_connection
        self.user_email = user_email
        self.initUI()
        self.chargerHistorique()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.zone_messages = QTextEdit()
        self.zone_messages.setReadOnly(True)
        self.message_edit = QLineEdit()
        self.envoyer_btn = QPushButton('Envoyer')

        layout.addWidget(self.zone_messages)
        layout.addWidget(self.message_edit)
        layout.addWidget(self.envoyer_btn)

        self.envoyer_btn.clicked.connect(self.envoyerMessage)

        self.setGeometry(300, 300, 400, 500)
        self.setWindowTitle('Chat Amélioré')
        self.appliquerStyles()

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
                    print(f"Erreur lors de l'enregistrement du message: {e}")

    def recupererIdUtilisateur(self):
        with self.db_connection.cursor() as cursor:
            query = "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            result = cursor.fetchone()
            return result[0] if result else None

    def chargerHistorique(self):
        id_utilisateur = self.recupererIdUtilisateur()
        if id_utilisateur is not None:
            with self.db_connection.cursor() as cursor:
                try:
                    query = "SELECT contenu, date_publication FROM Messages WHERE id_utilisateur=%s ORDER BY date_publication ASC"
                    cursor.execute(query, (id_utilisateur,))
                    for contenu, date_publication in cursor:
                        self.afficherMessage(contenu, "Historique")
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'historique: {e}")

    def appliquerStyles(self):
        self.setStyleSheet("""
            QTextEdit, QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #007bff;
                border-color: #007bff;
                color: white;
                padding: 6px 12px;
                margin-top: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
        """)
