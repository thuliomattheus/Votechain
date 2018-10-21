#include "../headers/block.h"

Block::Block(Document& d, string pH, int i)
    : data(d), previousHash(pH), index(i){
    this->timestamp = system_clock::to_time_t(system_clock::now());
    this->nonce = 0;
    this->setHash();
}

string Block::getHash(){
    return this->hash;
}

string Block::getPreviousHash(){
    return this->previousHash;
}

string Block::getTimestampAsString(){
    stringstream ss;
    ss << put_time(localtime(&this->timestamp), "%d/%m/%y - %T");
    return ss.str();
}

string Block::getAttributesAsString(){
    return to_string(this->index) + StringUtil::documentToString(this->data) + this->previousHash +
        this->getTimestampAsString() + to_string(this->nonce);
}

void Block::setHash(){
    this->hash = StringUtil::applySha256(this->getAttributesAsString());
}

void Block::showFullData(){
    cout << "Índice        : " << this->index << endl;
    cout << "Dados         : " << StringUtil::documentToString(this->data) << endl;
    cout << "Hash Anterior : " << this->previousHash << endl;
    cout << "Timestamp     : " << this->getTimestampAsString() << endl;
    cout << "Nonce         : " << this->nonce << endl;
    cout << "Hash Atual    : " << this->hash << "\n" << endl;
}
