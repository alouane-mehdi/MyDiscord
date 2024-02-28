from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from datetime import datetime

class ChatFenetre(QWidget):
    def __init__(self, prenom=''):
        super().__init__()
        self.prenom = prenom  # Stocke le prénom de l'utilisateur
        self.initUI()

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

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Chat')

    def envoyerMessage(self):
        message = self.message_edit.text()
        if message:  # Assurez-vous que le message n'est pas vide
            # Obtenez le timestamp actuel
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_message = f"[{timestamp}] {self.prenom}: {message}"  # Ajoutez le timestamp et le prénom au message
            self.afficherMessage(formatted_message)
            self.message_edit.clear()

    def afficherMessage(self, message):
        self.zone_messages.append(message)

