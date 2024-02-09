# chat_window.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from utilisateur import Utilisateur  # Assurez-vous que ce fichier est importé correctement

class ChatWindow(QMainWindow):
    def __init__(self, utilisateur, canal, db_connection):
        super().__init__()
        self.utilisateur = utilisateur
        self.canal = canal
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Créer les champs de saisie pour les informations de l'utilisateur
        self.nom_edit = QLineEdit(self)
        self.prenom_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        self.mdp_edit = QLineEdit(self)
        self.mdp_edit.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe
        self.ajouter_btn = QPushButton('Ajouter Utilisateur', self)

        # Ajouter les champs et le bouton au layout
        layout.addWidget(QLabel('Nom'))
        layout.addWidget(self.nom_edit)
        layout.addWidget(QLabel('Prénom'))
        layout.addWidget(self.prenom_edit)
        layout.addWidget(QLabel('Email'))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel('Mot de passe'))
        layout.addWidget(self.mdp_edit)
        layout.addWidget(self.ajouter_btn)

        # Connecter le bouton à la fonction d'ajout d'utilisateur
        self.ajouter_btn.clicked.connect(self.ajouterUtilisateur)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Chat')

    def ajouterUtilisateur(self):
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()

        utilisateur = Utilisateur(nom, prenom, email)
        try:
            utilisateur.ajouter_utilisateur(self.db_connection, mdp)
            QMessageBox.information(self, 'Succès', 'Utilisateur ajouté avec succès!')
            # Effacer les champs après l'ajout
            self.nom_edit.clear()
            self.prenom_edit.clear()
            self.email_edit.clear()
            self.mdp_edit.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'ajout de l\'utilisateur: {e}')







