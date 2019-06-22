from datetime import datetime
from hashlib import sha256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import b64encode
from random import randint
from sys import maxsize
import socket

def dateToString(date):
    return date.strftime('%d/%m/%y - %H:%M:%S %Z%z')

def stringToDate(string):
    return datetime.strptime(string, '%d/%m/%y - %H:%M:%S %Z%z')

def concatenate(objList):
    result = ""
    for obj in objList:
        result += str(obj)
    return result

def encryptSha256(message):
    return sha256(message.encode('utf-8')).hexdigest()

def getIpAndPort(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    local_ip_address = s.getsockname()[0]

    return local_ip_address, request.META['SERVER_PORT']

def isAddressValid(url):
    try:
        # Caso exista um ip e uma porta
        if(len(url.split(':'))==2):
            ip, port = url.split(':')
        else:
            return False

        # Divida o ip em suas partes
        ipParts = ip.split('.')

        # Verifique se o ip possui 4 partes
        # Se todas estão entre 0 e 255
        # E se a porta está entre 0 e 65535
        if(len(ipParts)==4 and
            (part.isdigit() and 0 <= int(part) < 256 for part in ipParts) and
            0 <= int(port) < 65536):
            return True
        else:
            return False
    except Exception:
        return False

"""
def criptografar(mensagem):
    # Cria um objeto para armazenar a mensagem
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Converte o objeto para byte
    digest.update(mensagem.encode('utf-8'))
    # Gera um número randômico, utilizando os limites do tipo 'int' como intervalo
    #salt = randint(-maxsize - 1, maxsize)
    # Concatena o salt com a mensagem
    #digest.update(str(salt).encode('utf-8'))
    # Retorna o salt e a mensagem criptografada
    #return salt, b64encode(digest.finalize()).decode('utf-8')
    return b64encode(digest.finalize()).decode('utf-8')
"""
