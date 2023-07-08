#TCP - La roue romaine

import socket
import time
import math
import re
import threading
import base64
import codecs


# Paramètres de connexion au challenge
host = 'challenge01.root-me.org'
port = 52021

# Fonction pour résoudre le défi
def solve_challenge():
    # Fonction pour recevoir la confirmation du serveur
    def receive_response():
        response = sock.recv(1024).decode()
        print("Réponse du serveur:", response)

    # Se connecter au serveur
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Recevoir le calcul du serveur
    data = sock.recv(1024).decode()
    print("Calcul reçu:", data)
    clear_content = re.search(r"'(.*?)'", data).group(1)

    print(clear_content)
    
    decoded_string = codecs.decode(clear_content, 'rot_13')


    sock.send((str(decoded_string)+"\n").encode())
    print("Réponse envoyée:", str(decoded_string))
    # Lancer un thread pour recevoir la confirmation du serveur
    response_thread = threading.Thread(target=receive_response)
    response_thread.start()

    # Attendre que le thread de réponse se termine
    response_thread.join()


    # Fermer la connexion
    sock.close()



solve_challenge()
