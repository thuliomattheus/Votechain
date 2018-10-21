#include "../headers/wallet.h"

Wallet::Wallet(string name, string cpf, string voterTitle){

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

RSA::PublicKey Wallet::getPublicKey(){

	return this->pubKey;

}

string Wallet::getName(){

	return this->name;
}

Transaction Wallet::toVote(RSA::PublicKey candidate){

	Transaction v(this->pubKey, candidate, this->privKey);

	return v;

}

void Wallet::updateBlockchain(Blockchain b){
	if(b.deep > this->blockchain.deep){
		this->blockchain = b;
	}
}

// string Wallet::getPublicKeyAsString(){

// 	return StringUtil::pubKeyAsString(this->pubKey);

// }


// string Wallet::getPrivateKeyAsString(){

// 	return StringUtil::privKeyAsString(this->privKey);

// }

void Wallet::teste(){

	const char* json =  "[{\"name\": \"Eden Hazard\",\"team\": \"chelsea\"},{\"name\": \"N'golo Kanté\",\"team\": \"chelsea\"}]";

	Document d;
	d.Parse(json);

	this->blockchain.showBlocks();
	cout << (this->blockchain.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

	this->blockchain.addBlock(d);
	this->blockchain.showBlocks();
	cout << (this->blockchain.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");
	this->blockchain.proofOfWork(this->blockchain.deep-1, this->blockchain.difficulty);
	this->blockchain.showBlocks();
	cout << (this->blockchain.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

	this->blockchain.addBlock(d);
	this->blockchain.showBlocks();
	cout << (this->blockchain.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");
	this->blockchain.proofOfWork(this->blockchain.deep-1, this->blockchain.difficulty);
	this->blockchain.showBlocks();
	cout << (this->blockchain.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

	// this->blockchain.addBlock("{Jogador : Marcos Alonso}");
	// this->blockchain.showBlocks();
	// cout << (this->blockchain.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

//     cout << (u.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");
//     u.chain.back().mineBlock(u.difficulty);
//     u.showBlocks();
//     cout << (u.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

//     Wallet meuPerfil, outroPerfil;

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
	Wallet eu("meu nome", "meu cpf", "meu titulo");

	eu.teste();

	const char* json =  "[{\"name\": \"Eden Hazard\",\"team\": \"chelsea\"},{\"name\": \"N'golo Kanté\",\"team\": \"chelsea\"}]";

	Document d;
	d.Parse(json);
	
	cout << StringUtil::documentToString(d) << endl;

	// Value& s = d[1]["name"];
	// cout << s.GetString() << endl;

	return 0;

}

// https://fullstack-developer.academy/blockchain-implementation-using-javascript/
// https://medium.com/@lhartikk/a-blockchain-in-200-lines-of-code-963cc1cc0e54
// https://medium.com/programmers-blockchain/creating-your-first-blockchain-with-java-part-2-transactions-2cdac335e0ce
// https://medium.com/@mycoralhealth/code-your-own-blockchain-in-less-than-200-lines-of-go-e296282bcffc

// https://bitcoin.org/en/developer-documentation
// https://www.investopedia.com/news/how-bitcoin-works/
// https://www.guru99.com/blockchain-tutorial.html
