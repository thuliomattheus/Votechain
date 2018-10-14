#include "../headers/voteBlock.h"

VoteBlock::VoteBlock(string data, string previousHash, int index){
    this->index = index;
    this->data = data;
    this->previousHash = previousHash;
    this->timestamp = system_clock::to_time_t(system_clock::now());
    this->nonce = 0;
    this->setHash();
}

string VoteBlock::getHash(){
    return this->hash;
}

string VoteBlock::getPreviousHash(){
    return this->previousHash;
}

string VoteBlock::getTimestampAsString(){
    stringstream ss;
    ss << put_time(localtime(&this->timestamp), "%d/%m/%y - %T");
    return ss.str();
}

string VoteBlock::getAttributesAsString(){
    return to_string(this->index) + this->data + this->previousHash +
        this->getTimestampAsString() + to_string(this->nonce);
}

void VoteBlock::setHash(){
    StringUtil su;
    this->hash = su.applySha256(this->getAttributesAsString());
}

void VoteBlock::showFullData(){
    cout << "Índice        : " << this->index << endl;
    cout << "Dados         : " << this->data << endl;
    cout << "Hash Anterior : " << this->previousHash << endl;
    cout << "Timestamp     : " << this->getTimestampAsString() << endl;
    cout << "Nonce         : " << this->nonce << endl;
    cout << "Hash Atual    : " << this->hash << "\n" << endl;
}

void VoteBlock::mineBlock(int difficulty){

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
