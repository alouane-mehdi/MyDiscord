from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class ChatFenetre(QWidget):
    def __init__(self):
        super().__init__()
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

        self.setWindowTitle('Chat')

    def envoyerMessage(self):
        message = self.message_edit.text()
        self.afficherMessage(message)
        self.message_edit.clear()

    def afficherMessage(self, message):
        self.zone_messages.append(message)
