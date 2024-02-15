import socket
import threading

IP = "127.0.0.1"
PORT = 55559

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connexion au server 

client.connect((IP, PORT))

#demander le pseudo au client

pseudo = input("Entrée votre pseudo")

# envoie du pseudo au server 
client.send(bytes(pseudo, "utf-8"))

#fonction pour envoyer un messages

def envoyerMessage():

    while True:

        message = input()
        #envoie du message au server
        client.send(bytes(message, "utf-8"))

        if message == "exit":
            break


#fonction pour recevoir les messages du server
        
def recevoirMessage():

    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(message)

        except:
                break

thread_envoie = threading.Thread(target=envoyerMessage)
thread_receptionMessage = threading.Thread(target=recevoirMessage)

thread_envoie.start()
thread_receptionMessage.start()











                


        