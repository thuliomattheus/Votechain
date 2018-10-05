#include "cryptoppLib.h"

void CryptoppLib::generatePairKey(){

	// Gerador de número aleatório
	AutoSeededRandomPool rng;

	// Declaração da chave privada
	RSA::PrivateKey privKey;

	// Criação da chave privada utilizando 3072 bits
	privKey.GenerateRandomWithKeySize(rng, 3072);

	// Criação da chave pública da chave privada criada
	RSA::PublicKey pubKey(privKey);

	// Criação dos arquivos que guardarão as chaves codificados utilizando base64
	Base64Encoder privKeySink(new FileSink("keys/privKey.txt"));
	Base64Encoder pubKeySink(new FileSink("keys/pubKey.txt"));

	// Copia a chave privada para o arquivo 'privkey.txt'
	privKey.DEREncode(privKeySink);
	pubKey.DEREncode(pubKeySink);

    // Necessário para finalizar a escrita das chaves
	privKeySink.MessageEnd();
    pubKeySink.MessageEnd();

    string privKeyAsString, pubKeyAsString;

    FileSource file1("keys/pubKey.txt", true, new StringSink (pubKeyAsString));
    FileSource file2("keys/privKey.txt", true, new StringSink (privKeyAsString));

    cout << pubKeyAsString << endl << endl;
    cout << privKeyAsString;

}

// int main(){

//     CryptoppLib teste;

//     teste.generatePairKey();

//     return 0;
// }

