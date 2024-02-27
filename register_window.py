from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from utilisateur import Utilisateur
from chat_window import ChatWindow

class RegisterWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Inscription')
        self.setGeometry(300, 300, 300, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.nom_edit = QLineEdit(self)
        self.prenom_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        self.mdp_edit = QLineEdit(self)
        self.mdp_edit.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel('Nom'))
        layout.addWidget(self.nom_edit)
        layout.addWidget(QLabel('Prénom'))
        layout.addWidget(self.prenom_edit)
        layout.addWidget(QLabel('Email'))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel('Mot de passe'))
        layout.addWidget(self.mdp_edit)

        self.register_btn = QPushButton('S\'inscrire', self)
        self.register_btn.clicked.connect(self.registerUser)
        layout.addWidget(self.register_btn)

    def registerUser(self):
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()

        if nom and prenom and email and mdp:
            utilisateur = Utilisateur(nom, prenom, email)
            try:
                utilisateur.ajouter_utilisateur(self.db_connection, mdp)
                QMessageBox.information(self, 'Succès', 'Utilisateur enregistré avec succès!')
                self.close()

                # Ouvrir la fenêtre de chat pour l'utilisateur inscrit
                chat_window = ChatWindow(utilisateur, None, self.db_connection)  # 'None' pour le canal
                chat_window.show()
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'inscription: {e}')
        else:
            QMessageBox.warning(self, 'Attention', 'Tous les champs doivent être remplis.')
