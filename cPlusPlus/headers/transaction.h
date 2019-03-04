#ifndef vote_h
#define vote_h

#include <iostream>

#include "utilities.h"
    using Utilities::StringUtil;

using namespace std;

class Transaction{

    public:
        string transactionId;
        RSA::PublicKey elector;
        RSA::PublicKey candidate;
        SecByteBlock signature;

        Transaction(RSA::PublicKey from, RSA::PublicKey to, RSA::PrivateKey me);
        void generateSignature(RSA::PrivateKey pvK);
        bool verifySignature();

    private:
        string calculateHash();


};

#endif