import socket
import time
import math
import re
import threading

# Paramètres de connexion au challenge
host = 'challenge01.root-me.org'
port = 52002

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

    # Expression régulière pour trouver les nombres
    pattern = r"Calculate the square root of (\d+) and multiply by (\d+)"

    matches = re.search(pattern, data)
    if matches:
        num1 = int(matches.group(1))
        num2 = int(matches.group(2))

        # Affichage des nombres extraits
        print("Num1:", num1)
        print("Num2:", num2)

        result = math.sqrt(num1) * num2
        rounded_result = round(result, 2)
        # Envoyer la réponse au serveur

        sock.send((str(rounded_result)+"\n").encode())
        print("Réponse envoyée:", str(rounded_result))

        # Lancer un thread pour recevoir la confirmation du serveur
        response_thread = threading.Thread(target=receive_response)
        response_thread.start()

        # Attendre que le thread de réponse se termine
        response_thread.join()

    # Fermer la connexion
    sock.close()



solve_challenge()
