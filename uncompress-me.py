#TCP - Uncompress Me
import socket
import time
import re
import base64
import zlib


# Paramètres de connexion au challenge
host = 'challenge01.root-me.org'
port = 52022

# Fonction auxiliaire récursive pour résoudre un défi individuel
def solve_challenge(sock, decoded_string):
    # Envoyer la réponse au serveur
    sock.send((str(decoded_string) + "\n").encode())
    print("Réponse envoyée:", str(decoded_string))

    # Attendre un court instant pour laisser le serveur envoyer la prochaine question
    time.sleep(0.5)

    try:
        # Recevoir la réponse du serveur
        response = sock.recv(1024).decode()
        print("Réponse du serveur:", response)
    except socket.timeout:
        print("Timeout lors de la réception de la réponse du serveur")
        return

    # Extraire la prochaine chaîne à décoder
    clear_content = re.search(r"'(.*?)'", response).group(1)
    decoded_string = zlib.decompress(base64.b64decode(clear_content)).decode('utf-8')

    # Résoudre le défi suivant récursivement
    solve_challenge(sock, decoded_string)


# Fonction pour résoudre les défis de manière itérative
def solve_challenge_iterative():
    # Se connecter au serveur
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Définir une limite de temps de 15 secondes pour la réception des données
    sock.settimeout(15)

    max_challenges = 5  # Nombre maximum de défis à résoudre

    # Recevoir le calcul initial du serveur
    data = sock.recv(1024).decode()
    print("Calcul reçu:", data)
    clear_content = re.search(r"'(.*?)'", data).group(1)
    decoded_string = zlib.decompress(base64.b64decode(clear_content)).decode('utf-8')

    # Appeler la fonction auxiliaire pour résoudre les défis de manière itérative
    solve_challenge(sock, decoded_string)

    # Fermer la connexion
    sock.close()

solve_challenge_iterative()
