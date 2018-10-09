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
        // byte signature[];

        Vote(RSA::PublicKey from, RSA::PublicKey to);
        void showHash();


    private:
        string calculateHash();

};

#endif