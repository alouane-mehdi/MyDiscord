from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from utilisateur import Utilisateur
from chat_fenetre import ChatFenetre

class ChatWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.email_edit = QLineEdit(self)
        self.email_edit.setPlaceholderText("Email")
        self.mdp_edit = QLineEdit(self)
        self.mdp_edit.setPlaceholderText("Mot de passe")
        self.mdp_edit.setEchoMode(QLineEdit.Password)
        self.prenom_edit = QLineEdit(self)
        self.prenom_edit.setPlaceholderText("Prénom")
        self.nom_edit = QLineEdit(self)
        self.nom_edit.setPlaceholderText("Nom")
        self.connexion_btn = QPushButton('Connexion', self)
        self.enregistrement_btn = QPushButton('Enregistrement', self)

        self.layout.addWidget(QLabel('Email'))
        self.layout.addWidget(self.email_edit)
        self.layout.addWidget(QLabel('Mot de passe'))
        self.layout.addWidget(self.mdp_edit)
        self.layout.addWidget(QLabel('Prénom'))
        self.layout.addWidget(self.prenom_edit)
        self.layout.addWidget(QLabel('Nom'))
        self.layout.addWidget(self.nom_edit)
        self.layout.addWidget(self.connexion_btn)
        self.layout.addWidget(self.enregistrement_btn)

        self.connexion_btn.clicked.connect(self.connecterUtilisateur)
        self.enregistrement_btn.clicked.connect(self.enregistrerUtilisateur)

        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle('Connexion - Chat')
        self.appliquerStyles()

    def appliquerStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #36393f;
            }
            QLineEdit {
                background-color: #202225;
                color: #ffffff;
                border: 1px solid #202225;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #7289da;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
            QLabel {
                color: #ffffff;
            }
        """)

    def connecterUtilisateur(self):
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()
        if Utilisateur.verifier_connexion(self.db_connection, email, mdp):
            self.hide()
            prenom = Utilisateur.recuperer_prenom(self.db_connection, email)
            self.chat_fenetre = ChatFenetre(prenom=prenom, db_connection=self.db_connection, user_email=email)
            self.chat_fenetre.show()
        else:
            QMessageBox.critical(self, 'Erreur', 'Email ou mot de passe incorrect.')

    def enregistrerUtilisateur(self):
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()
        prenom = self.prenom_edit.text()
        nom = self.nom_edit.text()
        utilisateur = Utilisateur(email=email, prenom=prenom, nom=nom)
        try:
            utilisateur.ajouter_utilisateur(self.db_connection, mdp)
            QMessageBox.information(self, 'Succès', 'Utilisateur enregistré avec succès!')
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'enregistrement: {e}')