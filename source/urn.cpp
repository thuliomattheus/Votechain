#include "../headers/urn.h"

Urn::Urn(){
    this->deep = 0;
}

void Urn::addBlock(string data){
    if(this->deep == 0){
        this->createGenesisBlock(data);
    }
    else{
        this->chain.push_back(VoteBlock(data, this->chain.back().getHash()));
        this->deep++;
    }
}

void Urn::createGenesisBlock(string data){
    this->chain.push_back(VoteBlock(data, this->genesisPreviousHash));
    this->deep++;
}

void Urn::showBlocks(){
    for(vector<VoteBlock>::iterator n=this->chain.begin(); n!=this->chain.end(); n++){
        n->showFullData();
    }
}

bool Urn::isChainValid(){

    string target(difficulty, '0');
    StringUtil calcHash;
    string aux;

    for(int i=0; i<this->deep; i++){

        VoteBlock b1 = this->chain[i];
        aux = calcHash.applySha256(b1.getAttributesAsString());

        if(i!=0){
            VoteBlock b0 = this->chain[i-1];

            if( b1.getHash() != aux ){
                return false;
            }
            if( b1.getPreviousHash() != b0.getHash() ){
                return false;
            }
            if( b1.getHash().substr(0, this->difficulty) !=  target){
                return false;
            }
        }
        else{
            if( b1.getHash() !=  aux ){
                return false;
            }
            if(b1.getPreviousHash() != this->genesisPreviousHash){
                return false;
            }
            if( b1.getHash().substr(0, this->difficulty) !=  target){
                return false;
            }
        }

    }
    return true;
}

// https://fullstack-developer.academy/blockchain-implementation-using-javascript/
// https://medium.com/@lhartikk/a-blockchain-in-200-lines-of-code-963cc1cc0e54
// https://medium.com/programmers-blockchain/creating-your-first-blockchain-with-java-part-2-transactions-2cdac335e0ce