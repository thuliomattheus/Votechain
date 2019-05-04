from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64

def generateKeys():

    # Geração da chave privada
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serialização e decodificação da chave privada
    privateKey = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    # Geração, serialização e decodificação da chave pública
    publicKey = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1,
    ).decode('utf-8')

    return privateKey, publicKey

def signMessage(privateKey, message):

    # Converte a chave de string para byte
    private_key = privateKey.encode('utf-8')

    # Deserializa a chave privada
    private_key = serialization.load_pem_private_key(
        data=private_key,
        password=None,
        backend=default_backend()
    )

    # Assina a mensagem com a chave privada
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return str(base64.b64encode(signature), encoding='utf-8')

def verifySignature(signature, message, senderPublicKey):

    # Converte a chave de string para byte
    public_key = senderPublicKey.encode('utf-8')

    # Deserializa a chave pública
    public_key = serialization.load_pem_public_key(
        data=public_key,
        backend=default_backend()
    )

    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True

    except InvalidSignature:
        return False
