from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from utilisateur import Utilisateur
from chat_fenetre import ChatFenetre 

class ChatWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.email_edit = QLineEdit(self)
        self.mdp_edit = QLineEdit(self)
        self.mdp_edit.setEchoMode(QLineEdit.Password)
        self.connexion_btn = QPushButton('Connexion', self)
        self.enregistrement_btn = QPushButton('Enregistrement', self)

        layout.addWidget(QLabel('Email'))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel('Mot de passe'))
        layout.addWidget(self.mdp_edit)
        layout.addWidget(self.connexion_btn)
        layout.addWidget(self.enregistrement_btn)

        self.connexion_btn.clicked.connect(self.connecterUtilisateur)
        self.enregistrement_btn.clicked.connect(self.enregistrerUtilisateur)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Chat')

    def enregistrerUtilisateur(self):
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()
        utilisateur = Utilisateur(email=email)
        try:
            utilisateur.ajouter_utilisateur(self.db_connection, mdp)
            QMessageBox.information(self, 'Succès', 'Utilisateur enregistré avec succès!')
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'enregistrement: {e}')

    def connecterUtilisateur(self):
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()
        if Utilisateur.verifier_connexion(self.db_connection, email, mdp):
            self.hide()  # Cachez ou fermez la fenêtre de connexion
            self.chat_fenetre = ChatFenetre()
            self.chat_fenetre.show()
        else:
            QMessageBox.critical(self, 'Erreur', 'Email ou mot de passe incorrect.')
