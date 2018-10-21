#include "../headers/transaction.h"

Transaction::Transaction(RSA::PublicKey from, RSA::PublicKey to, RSA::PrivateKey me){
    this->elector = from;
    this->candidate = to;

    this->generateSignature(me);
}

string Transaction::calculateHash(){

    string elector = StringUtil::pubKeyAsString(this->elector);
    string candidate = StringUtil::pubKeyAsString(this->candidate);

    return StringUtil::applySha256(elector+candidate);
}

void Transaction::generateSignature(RSA::PrivateKey pvK){

    string elector = StringUtil::pubKeyAsString(this->elector);
    string candidate = StringUtil::pubKeyAsString(this->candidate);

    this->signature = StringUtil::signMessage(pvK, elector+candidate);
}

bool Transaction::verifySignature(){

    string elector = StringUtil::pubKeyAsString(this->elector);
    string candidate = StringUtil::pubKeyAsString(this->candidate);

    return StringUtil::verifyMessage(this->elector, elector+candidate, this->signature);
}
