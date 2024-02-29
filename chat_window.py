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

        # Champs pour l'email et le mot de passe
        self.email_edit = QLineEdit(self)
        self.mdp_edit = QLineEdit(self)
        self.mdp_edit.setEchoMode(QLineEdit.Password)

        # Ajout des champs pour le prénom et le nom
        self.prenom_edit = QLineEdit(self)
        self.nom_edit = QLineEdit(self)

        # Boutons de connexion et d'enregistrement
        self.connexion_btn = QPushButton('Connexion', self)
        self.enregistrement_btn = QPushButton('Enregistrement', self)

        # Ajout des widgets au layout
        layout.addWidget(QLabel('Email'))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel('Mot de passe'))
        layout.addWidget(self.mdp_edit)
        layout.addWidget(QLabel('Prénom'))
        layout.addWidget(self.prenom_edit)
        layout.addWidget(QLabel('Nom'))
        layout.addWidget(self.nom_edit)
        layout.addWidget(self.connexion_btn)
        layout.addWidget(self.enregistrement_btn)

        # Connexion des boutons à leurs fonctions respectives
        self.connexion_btn.clicked.connect(self.connecterUtilisateur)
        self.enregistrement_btn.clicked.connect(self.enregistrerUtilisateur)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Chat')

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

    def connecterUtilisateur(self):
        email = self.email_edit.text()
        mdp = self.mdp_edit.text()
        if Utilisateur.verifier_connexion(self.db_connection, email, mdp):
            self.hide() 
            prenom = Utilisateur.recuperer_prenom(self.db_connection, email)
            self.chat_fenetre = ChatFenetre(prenom=prenom, db_connection=self.db_connection, user_email=email)
            self.chat_fenetre.chargerHistorique()
            self.chat_fenetre.show()
        else:
            QMessageBox.critical(self, 'Erreur', 'Email ou mot de passe incorrect.')
