from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from base64 import b64encode, b64decode

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
    )

    # Geração, serialização e decodificação da chave pública
    publicKey = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1,
    )

    return privateKey.decode('utf-8'), publicKey.decode('utf-8')

def signMessage(privateKey, message):

    # Converte chave e mensagem, de string para byte
    encoded_private_key = privateKey.encode('utf-8')
    encoded_message = message.encode('utf-8')

    # Deserializa a chave privada
    deserialized_private_key = serialization.load_pem_private_key(
        data=encoded_private_key,
        password=None,
        backend=default_backend()
    )

    # Assina a mensagem com a chave privada
    signature = deserialized_private_key.sign(
        encoded_message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return b64encode(signature).decode('utf-8')

def verifySignature(signature, message, senderPublicKey):

    # Converte chave e mensagem, de string para byte
    encoded_public_key = senderPublicKey.encode('utf-8')
    encoded_message = message.encode('utf-8')

    try:
        decoded_signature = b64decode(signature)
    except:
        print("Assinatura não pôde ser decodificada!")
        return False

    try:
        # Deserializa a chave pública
        deserialized_public_key = serialization.load_pem_public_key(
            data=encoded_public_key,
            backend=default_backend()
        )
    except ValueError:
        print("Não dá pra deserializar os dados!")
        return False

    try:
        deserialized_public_key.verify(
            decoded_signature,
            encoded_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True

    except InvalidSignature:
        print("Assinatura inválida!")
        return False
