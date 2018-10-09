#include "../headers/electorArea.h"

ElectorArea::ElectorArea(){

	// Gerador de número aleatório
	AutoSeededRandomPool rng;

	// Criação da chave privada utilizando 3072 bits
	this->privKey.GenerateRandomWithKeySize(rng, 3072);

	// Utilização de uma variável auxiliar para guardar o valor
	RSA::PublicKey aux(this->privKey);

	// Criação da chave pública utilizando a chave privada
	this->pubKey = aux;

}

RSA::PublicKey ElectorArea::getPublicKey(){

	return this->pubKey;

}

string ElectorArea::getPublicKeyAsString(){

	StringUtil su;

	return su.pubKeyAsString(this->pubKey);

}


string ElectorArea::getPrivateKeyAsString(){

	StringUtil su;

	return su.privKeyAsString(this->privKey);

}

void ElectorArea::testarAssinaturas(RSA::PublicKey pubK){
	StringUtil su;

	SecByteBlock sbb = su.signMessage(this->privKey, "Hazard é o 10 do Chelsea");

	cout << "\n\n" << su.verifyMessage(pubK, "Hazard é o 10 do Chelsea", sbb) << endl;
}