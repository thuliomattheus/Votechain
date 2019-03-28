from datetime import datetime
from hashlib import sha256

def dateToString(date):
    return date.strftime("%d/%m/%y - %T %z")

def concatenate(objList):
    result = ""
    for obj in objList:
        result += str(obj)
    return result

def encryptSha256(message):
    return sha256(message.encode()).hexdigest()
