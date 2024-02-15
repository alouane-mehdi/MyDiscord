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

def diffuser(message):
    for client in clients:
        client.send(bytes(message,"utf-8"))

def gestionConnexion():

    while True:
        client, adress = server.accept()
        print(f"Connexion établie avec {str(adress)}")

        pseudo = client.recv(1024).decode("utf-8")

        #mettre un nouveau client dans la liste des clients
        clients.append(client)
        pseudos.append(pseudo)

    #message d'acceuille pour les clients
        print(f"{pseudo} a rejoint le chat")
        client.send(bytes("bienvenue dans le chat : \n", "utf-8"))
        diffuser(f"{pseudo} a rejoint le chat")

        thread_client = threading.Thread(target=gestion_client, args=(client,pseudo))
        thread_client.start()

#gerer les lessages envoyes par les client
def gestion_client(client,pseudo):
    while True:

        try:
            message = client.recv(1024).decode("utf-8")

            if message == "exit":
                index = clients.index(client)
                #si un client fait exit, la fonction supprime le client
                clients.remove(client)   
                client.close()
            #par la suite ont supprime le pseudo
                pseudo = pseudos[index]
                pseudos.remove(pseudo)

                diffuser(f"{pseudo} a quitter le chat")
                break

            else:   
                diffuser(f"{pseudo}: {message}")

        except:

               if message == "exit":
                index = clients.index(client)
                #si un client fait exit, la fonction supprime le client
                clients.remove(client)   
                client.close()
            #par la suite ont supprime le pseudo
                pseudo = pseudos[index]
                pseudos.remove(pseudo)

                diffuser(f"{pseudo} a quitter le chat")
                break
print("le serveur de chat est en marche !!!")              
gestionConnexion()
