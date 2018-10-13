#ifndef vote_h
#define vote_h

#include <iostream>

#include "stringUtil.h"

using namespace std;

class Vote{

    public:
        string voteId;
        RSA::PublicKey elector;
        RSA::PublicKey candidate;
        SecByteBlock signature;

        Vote(RSA::PublicKey from, RSA::PublicKey to, RSA::PrivateKey me);
        void generateSignature(RSA::PrivateKey pvK);
        bool verifySignature();

    private:
        string calculateHash();


};

#endif