#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <cryptopp/filters.h>
#include <cryptopp/hex.h>
#include <cryptopp/sha.h>
#include "block.h"

using namespace std;
using chrono::system_clock;

Block::Block(string data, string previousHash){
    this->data = data;
    this->previousHash = previousHash;
    this->timestamp = system_clock::to_time_t(system_clock::now());

    CryptoPP::SHA256 hash;
    string blockAttr = this->getData() + this->getPreviousHash() +
        this->getTimestampAsString();

	CryptoPP::StringSource s(blockAttr, true,
			new CryptoPP::HashFilter(hash,
				new CryptoPP::HexEncoder(
					new CryptoPP::StringSink(this->hash))));

    cout << this->hash << endl;
}

string Block::getData(){
    return this->data;
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

void Block::setData(string s){
    this->data = s;
}

void Block::setPreviousHash(string s){
    this->previousHash = s;
}

void Block::getAttributes(){
    cout << this->getData() << " " << this->getPreviousHash() << endl;
    cout << this->getTimestampAsString() << endl;
}


int main(){

    Block b0("Va embora", "arrombado da mulesta");
    b0.getAttributes();
    return 0;
}