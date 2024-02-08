import socket

# le module socket permet la programmation réseau, 
#c'est-à-dire la communication entre différents ordinateurs via un réseau

host, port = ('', 5599)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.bind((host,port))
print('le serveur est démarré')

while True:
    socket.listen(5)
    conn, address = socket.accept() 
    print("En écoute....")


conn.close()
socket.close()