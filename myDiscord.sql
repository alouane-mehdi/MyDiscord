CREATE DATABASE myDiscord;

USE myDiscord;

CREATE TABLE Utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    mot_de_passe VARCHAR(255),
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Canaux (
    id_canal INT AUTO_INCREMENT PRIMARY KEY,
    nom_canal VARCHAR(255),
    est_prive BOOLEAN DEFAULT FALSE
);

CREATE TABLE Messages (
    id_message INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT,
    id_canal INT,
    contenu TEXT,
    date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_canal) REFERENCES Canaux(id_canal)
);

CREATE TABLE Reactions (
    id_reaction INT AUTO_INCREMENT PRIMARY KEY,
    id_message INT,
    id_utilisateur INT,
    type_reaction VARCHAR(50),
    FOREIGN KEY (id_message) REFERENCES Messages(id_message),
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur)
);

CREATE TABLE DroitsAcces (
    id_droit INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT,
    id_canal INT,
    niveau_acces VARCHAR(50),
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_canal) REFERENCES Canaux(id_canal)
);

-- Insertion d'utilisateurs
INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe) VALUES
('Dupont', 'Jean', 'jean.dupont@email.com', 'password123'),
('Durand', 'Marie', 'marie.durand@email.com', 'password456');

-- Insertion de canaux
INSERT INTO Canaux (nom_canal, est_prive) VALUES
('Général', FALSE),
('Jeux', FALSE);

-- Assurez-vous de vérifier les id_utilisateur et id_canal corrects avant d'insérer des messages et des réactions
-- Insertion de messages
INSERT INTO Messages (id_utilisateur, id_canal, contenu) VALUES
(1, 1, 'Bonjour tout le monde !'),
(2, 1, 'Salut à tous, comment ça va ?');

-- Insertion de réactions (assurez-vous que les id_message sont corrects)
INSERT INTO Reactions (id_message, id_utilisateur, type_reaction) VALUES
(1, 2, '👍'),
(2, 1, '😀');

-- Insertion de droits d'accès
INSERT INTO DroitsAcces (id_utilisateur, id_canal, niveau_acces) VALUES
(1, 1, 'Administrateur'),
(2, 2, 'Membre');

