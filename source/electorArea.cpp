#include "../headers/electorArea.h"

ElectorArea::ElectorArea(string name, string cpf, string voterTitle){

	this->name = name;
	this->cpf = cpf;
	this->voterTitle = voterTitle;

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

string ElectorArea::getName(){

	cout << this->blockchain.deep << endl;
	return this->name;
}

Vote ElectorArea::toVote(RSA::PublicKey candidate){

	Vote v(this->pubKey, candidate, this->privKey);

	return v;

}

// string ElectorArea::getPublicKeyAsString(){

// 	StringUtil su;

// 	return su.pubKeyAsString(this->pubKey);

// }


// string ElectorArea::getPrivateKeyAsString(){

// 	StringUtil su;

// 	return su.privKeyAsString(this->privKey);

// }

void ElectorArea::teste(){
	this->blockchain.addBlock("{Jogador : Hazard}");
	this->blockchain.showBlocks();

//     cout << (u.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");
//     u.chain.back().mineBlock(u.difficulty);
//     u.showBlocks();
//     cout << (u.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

//     ElectorArea meuPerfil, outroPerfil;

//     Vote v = meuPerfil.toVote(outroPerfil.getPublicKey());

//     cout << (v.verifySignature() ? "O voto é válido\n\n" : "O voto é inválido\n\n");

//     // v.showHash();

//     // b.addBlock("{Jogador : Kanté}");
//     // b.chain.back().mineBlock(b.difficulty);
//     // b.addBlock("{Jogador : M. Alonso}");
//     // b.chain.back().mineBlock(b.difficulty);
//     // b.addBlock("{Jogador : Jorginho}");
//     // b.chain.back().mineBlock(b.difficulty);
//     // b.addBlock("{Jogador : Willian}");
//     // b.chain.back().mineBlock(b.difficulty);
//     // b.addBlock("{Jogador : Rudiger}");
//     // b.chain.back().mineBlock(b.difficulty);
//     // b.addBlock("{Jogador : D. Luiz}");
//     // b.chain.back().mineBlock(b.difficulty);
//     // b.addBlock("{Jogador : Barkley}");
//     // b.chain.back().mineBlock(b.difficulty);

//     // b.showBlocks();
//     // cout << b.isChainValid() ? "A blockchain é válida" : "A blockchain é inválida";

}

int main(){
	ElectorArea eu("meu nome", "meu cpf", "meu titulo");

	cout << eu.getName() << endl;

	eu.teste();

	cout << eu.getName() << endl;
}