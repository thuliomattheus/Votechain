#include "../headers/vote.h"

Vote::Vote(RSA::PublicKey from, RSA::PublicKey to){
    this->elector = from;
    this->candidate = to;
}

string Vote::calculateHash(){

    StringUtil su;

    string elector = su.pubKeyAsString(this->elector);
    string candidate = su.pubKeyAsString(this->candidate);

    return su.applySha256(elector+candidate);
}

void Vote::showHash(){
    cout << this->calculateHash() << endl;
}