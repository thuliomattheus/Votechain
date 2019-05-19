from datetime import datetime
from hashlib import sha256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import b64encode
from random import randint
from sys import maxsize
from clientProject.settings import PRIVATE_KEY_FILENAME, PRIVATE_KEY_PATH

def encryptSha256(message):
    return sha256(message.encode('utf-8')).hexdigest()

def writeMessageOnFile(message, filename=PRIVATE_KEY_FILENAME, path=PRIVATE_KEY_PATH):
    with open(str(path) + str(filename), 'w') as encryptedMessageFile:
        encryptedMessageFile.write(message) 

"""
def criptografar(mensagem):
    # Cria um objeto para armazenar a mensagem
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Converte o objeto para byte
    digest.update(mensagem.encode('utf-8'))
    # Gera um número randômico, utilizando os limites do tipo 'int' como intervalo
    salt = randint(-maxsize - 1, maxsize)
    # Concatena o salt com a mensagem
    digest.update(str(salt).encode('utf-8'))
    # Retorna o salt e a mensagem criptografada
    return salt, b64encode(digest.finalize()).decode('utf-8')
"""
