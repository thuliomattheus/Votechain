#include "../headers/vote.h"

Vote::Vote(RSA::PublicKey from, RSA::PublicKey to, RSA::PrivateKey me){
    this->elector = from;
    this->candidate = to;

    this->generateSignature(me);
}

string Vote::calculateHash(){

    StringUtil su;

    string elector = su.pubKeyAsString(this->elector);
    string candidate = su.pubKeyAsString(this->candidate);

    return su.applySha256(elector+candidate);
}

void Vote::generateSignature(RSA::PrivateKey pvK){
    StringUtil su;

    string elector = su.pubKeyAsString(this->elector);
    string candidate = su.pubKeyAsString(this->candidate);

    this->signature = su.signMessage(pvK, elector+candidate);
}

bool Vote::verifySignature(){
    StringUtil su;

    string elector = su.pubKeyAsString(this->elector);
    string candidate = su.pubKeyAsString(this->candidate);

    return su.verifyMessage(this->elector, elector+candidate, this->signature);
}
