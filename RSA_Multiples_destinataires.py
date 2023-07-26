from Crypto.PublicKey import RSA
from sympy import *
from functools import reduce
import base64
from Crypto.Util.number import inverse

def cuberoot(x):
    l = 0
    h = x
    while l < h:
        m = (l+h)//2
        if m*m*m < x:
            l = m+1
        else:
            h = m
    return l

def read_key(file):
    with open(file, 'r') as f:
        key = RSA.importKey(f.read())
    return key

def read_msg(file):
    with open(file, 'r') as f:
        msg = base64.b64decode(f.read().strip())
        msg = int.from_bytes(msg, byteorder='big')
    return msg

# Lecture des clés publiques et des messages
keys = [read_key(f'clef{i}_pub.pem') for i in range(3)]
msgs = [read_msg(f'm{i}') for i in range(3)]

# Vérifie que les exposants des clés sont tous égaux à 3
for key in keys:
    assert key.e == 3

# Calcule le produit des moduli
N = reduce(lambda x, y: x*y, (key.n for key in keys))

# Calcule le message chiffré
C = 0
for i in range(3):
    Mi = N // keys[i].n
    ti = inverse(Mi, keys[i].n)
    C += msgs[i] * Mi * ti
C %= N

# Le message original est la racine cubique du message chiffré
m = cuberoot(C)

# Convertir l'entier m en bytes et décodage
message = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

print(message)
