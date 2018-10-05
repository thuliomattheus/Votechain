#include "cryptoppLib.h"

void CryptoppLib::generatePairKeyAsString(string &pubK, string &privK){

	// Gerador de número aleatório
	AutoSeededRandomPool rng;

	// // Declaração da chave privada
	RSA::PrivateKey privKey;

	// Criação da chave privada utilizando 3072 bits
	privKey.GenerateRandomWithKeySize(rng, 3072);

	// Criação da chave pública da chave privada criada
	RSA::PublicKey pubKey(privKey);

	// Aponta o codificador de base64 para atuar sobre a string
	Base64Encoder privKeySink(new StringSink(privK));
	Base64Encoder pubKeySink(new StringSink(pubK));

	// Copia as chaves para as respectivas strings
	privKey.DEREncode(privKeySink);
	pubKey.DEREncode(pubKeySink);

    // Necessário para finalizar a escrita das chaves
	privKeySink.MessageEnd();
    pubKeySink.MessageEnd();

}