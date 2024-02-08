import socket

host, port = ('localhost', 5599)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    
    socket.connect((host, port))
    print("client connecté !")

except ConnectionRefusedError:

    print("connexion refusé")
finally:

    socket.close()