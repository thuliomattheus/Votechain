#include "block.h"

Block::Block(string data, string previousHash){
    this->data = data;
    this->previousHash = previousHash;
    this->timestamp = system_clock::to_time_t(system_clock::now());
    this->nonce = 0;
    this->setHash();
}

string Block::getData(){
    return this->data;
}

uint64_t Block::getNonce(){
    return this->nonce;
}

string Block::getHash(){
    return this->hash;
}

string Block::getPreviousHash(){
    return this->previousHash;
}

time_t Block::getTimestamp(){
    return this->timestamp;
}

string Block::getTimestampAsString(){
    stringstream ss;
    ss << put_time(localtime(&this->timestamp), "%d/%m/%y - %T");
    return ss.str();
}

string Block::getAttributesAsString(){
    return this->data + this->previousHash +
        this->getTimestampAsString() + to_string(this->nonce);
}

void Block::setHash(){
    this->hash = this->calculateHash(this->getAttributesAsString());
}

void Block::setPreviousHash(string s){
    this->previousHash = s;
}

void Block::setData(string s){
    this->data = s;
}

void Block::printFullDataAsString(){
    cout << "Dados         : " << this->getData() << endl;
    cout << "Hash Anterior : " << this->getPreviousHash() << endl;
    cout << "Timestamp     : " << this->getTimestampAsString() << endl;
    cout << "Nonce         : " << this->getNonce() << endl;
    cout << "Hash Atual    : " << this->getHash() << "\n" << endl;
}

string Block::calculateHash(string s){
    string hashed_s;

    SHA256 hash;

	StringSource ssource(s, true,
			new HashFilter(hash,
				new HexEncoder(
					new StringSink(hashed_s))));

    return hashed_s;
}

void Block::mineBlock(int difficulty){

    // Crie uma string de tamanho 'difficulty' composta apenas por zeros
    string target(difficulty, '0');

    auto startTime = high_resolution_clock::now();

    // Enquanto os primeiros 'difficulty' caracteres forem diferentes de 0
    while(this->hash.substr(0, difficulty) != target){
        nonce++;
        this->setHash();
    }
    auto endTime = high_resolution_clock::now();

    cout << "Bloco minerado em " << duration_cast<chrono::seconds>(endTime - startTime).count() << " segundos\n\n";
}
