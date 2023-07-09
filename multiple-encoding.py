import socket
import time
import re
import base64
import zlib


class ChallengeSolver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.encode_table = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "0": "-----",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            ".": ".-.-.-",
            ",": "--..--",
            "?": "..--..",
            " ": "SPACE",
        }
        # Reverse of encode_table.
        self.decode_table = {v: k for k, v in self.encode_table.items()}

    def is_base64_encoded(self, input_string):
        try:
            decoded_bytes = base64.b64decode(input_string)
            # Check if the decoded bytes can be properly decoded as a string
            decoded_string = decoded_bytes.decode('utf-8')
            # If the decoding was successful, it is likely Base64 encoded
            return True
        except (base64.binascii.Error, UnicodeDecodeError):
            # If an exception occurs during decoding, it is not Base64 encoded
            return False

    def is_morse(self, message):
        allowed_chars = '.-/'
        return all(ch in allowed_chars or ch.isspace() for ch in message)

    def is_hexadecimal(self, input_string):
        pattern = r'^[0-9a-fA-F]+$'
        return bool(re.match(pattern, input_string))

    def decode_hexadecimal(self, hex_string):
        try:
            bytes_data = bytes.fromhex(hex_string)
            decoded_string = bytes_data.decode('utf-8')
            return decoded_string
        except ValueError:
            return None

    def is_base85_encoded(self, input_string):
        try:
            decoded_bytes = base64.b85decode(input_string)
            decoded_string = decoded_bytes.decode('utf-8')
            return True
        except (base64.binascii.Error, UnicodeDecodeError):
            return False

    def decode_base85(self, base85_string):
        try:
            decoded_bytes = base64.b85decode(base85_string)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def decode_morse_code(self, encoded):
        symbols = encoded.split("/")
        return "".join(self.decode_table[x] for x in symbols if x in self.decode_table)

    def decode_ipv6(self, encoded_string):
        decoded = ""
        padding_count = encoded_string.count("z")

        # Remove padding characters 'z'
        stripped_string = encoded_string.replace("z", "")

        # Calculate the number of characters per group (5 bytes in IPv6 encoding)
        chars_per_group = 5

        # Iterate over the string in groups of characters
        for i in range(0, len(stripped_string), chars_per_group):
            group = stripped_string[i : i + chars_per_group]
            value = 0

            # Calculate the decimal value of the group
            for char in group:
                value = value * 85 + (ord(char) - 33)

            # Convert the decimal value to bytes and add to the decoded string
            decoded += value.to_bytes(4, "big")

        # Remove padding bytes based on the padding count
        decoded = decoded[:-padding_count]

        return decoded.decode("utf-8")

    def is_ipv6_encoded(self, input_string):
        # Check the string length
        if len(input_string) % 5 != 0:
            return False

        # Check for valid characters and patterns
        for char in input_string:
            if not (33 <= ord(char) <= 117 or char == "z"):
                return False

        # Check if the string starts with 'X' and ends with '<'
        if not (input_string.startswith("X") and input_string.endswith("<")):
            return False

        # Check if there are no repeated 'z' characters
        if "zz" in input_string:
            return False

        # Check if there are at least 5 valid characters in each group
        for i in range(0, len(input_string), 5):
            group = input_string[i : i + 5]
            if group.count("z") > 1:
                return False

        return True

    def is_base32_encoded(self, input_string):
        try:
            decoded_bytes = base64.b32decode(input_string, casefold=True)
            decoded_string = decoded_bytes.decode("utf-8")
            return True
        except (base64.binascii.Error, UnicodeDecodeError):
            return False

    def decode_base32(self, base32_string):
        try:
            decoded_bytes = base64.b32decode(base32_string, casefold=True)
            decoded_string = decoded_bytes.decode("utf-8")
            return decoded_string
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def solve_challenge(self, sock, decoded_string):
        # Envoyer la réponse au serveur
        sock.send((str(decoded_string) + "\n").encode())
        print("Réponse envoyée:", str(decoded_string))

        # Attendre un court instant pour laisser le serveur envoyer la prochaine question
        time.sleep(0.05)

        try:
            # Recevoir la réponse du serveur
            response = sock.recv(1024).decode()
            print("Réponse du serveur:", response)
        except socket.timeout:
            print("Timeout lors de la réception de la réponse du serveur")
            return

        # Extraire la prochaine chaîne à décoder
        clear_content = re.search(r"'(.*?)'", response).group(1)

        if self.is_base64_encoded(clear_content):
            decoded_string = base64.b64decode(clear_content).decode('utf-8')
        elif self.is_morse(clear_content):
            decoded_string = self.decode_morse_code(clear_content)
            decoded_string = decoded_string.lower()
        elif self.is_hexadecimal(clear_content):
            decoded_string = self.decode_hexadecimal(clear_content)
        elif self.is_base32_encoded(clear_content):
            decoded_string = self.decode_base32(clear_content)
        elif self.is_ipv6_encoded(clear_content):
            decoded_string = self.decode_ipv6(clear_content)
        elif self.is_base85_encoded(clear_content):
            decoded_string = self.decode_base85(clear_content)
        else:
            decoded_string = "shit"

        # Résoudre le défi suivant récursivement
        self.solve_challenge(sock, decoded_string)

    def solve_challenge_iterative(self):
        # Se connecter au serveur
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        # Définir une limite de temps de 15 secondes pour la réception des données
        sock.settimeout(15)

        max_challenges = 5  # Nombre maximum de défis à résoudre

        # Recevoir le calcul initial du serveur
        data = sock.recv(1024).decode()
        print("Calcul reçu:", data)
        clear_content = re.search(r"'(.*?)'", data).group(1)

        if self.is_base64_encoded(clear_content):
            decoded_string = base64.b64decode(clear_content).decode('utf-8')
        elif self.is_morse(clear_content):
            decoded_string = self.decode_morse_code(clear_content)
            decoded_string = decoded_string.lower()
        elif self.is_hexadecimal(clear_content):
            decoded_string = self.decode_hexadecimal(clear_content)
        elif self.is_base32_encoded(clear_content):
            decoded_string = self.decode_base32(clear_content)
        elif self.is_ipv6_encoded(clear_content):
            decoded_string = self.decode_ipv6(clear_content)
        elif self.is_base85_encoded(clear_content):
            decoded_string = self.decode_base85(clear_content)
        else:
            decoded_string = "shit"

        # Appeler la fonction auxiliaire pour résoudre les défis de manière itérative
        self.solve_challenge(sock, decoded_string)

        # Fermer la connexion
        sock.close()


# Utilisation de la classe pour résoudre les défis
solver = ChallengeSolver('challenge01.root-me.org', 52017)
solver.solve_challenge_iterative()
