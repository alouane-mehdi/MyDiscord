import socket
import threading

 #config du server

IP = '127.0.0.1'

PORT = 55559
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#config du server terminée 

#indication au server de l'ip et du port

server.bind((IP, PORT))

#définition du nombre maximum d'utilisateurs dans le server

server.listen(10)

# création de variables qui va stocker les clients/pseudo
clients = []
pseudos = []

import threading
import socket

class srv():
    clients = []   # Assurez-vous de déclarer ces listes en tant que variables de classe
    pseudos = []   # pour qu'elles soient partagées entre les méthodes de la classe

    @classmethod
    def diffuser(cls, message):
        for client in cls.clients:
            client.send(bytes(message, "utf-8"))

    @classmethod
    def gestionConnexion(cls):
        while True:
            client, address = server.accept()
            print(f"Connexion établie avec {str(address)}")

            pseudo = client.recv(1024).decode("utf-8")

            # Mettre un nouveau client dans la liste des clients
            cls.clients.append(client)
            cls.pseudos.append(pseudo)

            # Message d'accueil pour les clients
            print(f"{pseudo} a rejoint le chat")
            client.send(bytes("Bienvenue dans le chat : \n", "utf-8"))
            cls.diffuser(f"{pseudo} a rejoint le chat")

            thread_client = threading.Thread(target=cls.gestion_client, args=(client, pseudo))
            thread_client.start()

    # Gérer les messages envoyés par les clients
    @classmethod
    def gestion_client(cls, client, pseudo):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")

                if message == "exit":
                    index = cls.clients.index(client)
                    # Si un client fait exit, la fonction supprime le client
                    cls.clients.remove(client)
                    client.close()
                    # Par la suite, on supprime le pseudo
                    pseudo = cls.pseudos[index]
                    cls.pseudos.remove(pseudo)

                    cls.diffuser(f"{pseudo} a quitté le chat")
                    break

                else:
                    cls.diffuser(f"{pseudo}: {message}")

            except:
                if message == "exit":
                    index = cls.clients.index(client)
                    # Si un client fait exit, la fonction supprime le client
                    cls.clients.remove(client)
                    client.close()
                    # Par la suite, on supprime le pseudo
                    pseudo = cls.pseudos[index]
                    cls.pseudos.remove(pseudo)

                    cls.diffuser(f"{pseudo} a quitté le chat")
                    break

print("Le serveur de chat est en marche !!!")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 55558))
server.listen(5)

srv.gestionConnexion()
