#ifndef electorArea_h
#define electorArea_h

#include <iostream>
    using namespace std;

#include "urn.h"
#include "vote.h"
#include "stringUtil.h"

#include "../lib/cryptopp/rsa.h"
    using CryptoPP::RSA;

#include "../lib/cryptopp/osrng.h"
    using CryptoPP::AutoSeededRandomPool;

class ElectorArea{

    private:

        string name;
        string cpf;
        string voterTitle;
    	RSA::PrivateKey privKey;
    	RSA::PublicKey pubKey;
        Urn blockchain;

        // string getPrivateKeyAsString();
        // string getPublicKeyAsString();

    public:

        ElectorArea(string name, string cpf, string voterTitle);

        string getName();

        RSA::PublicKey getPublicKey();

        Vote toVote(RSA::PublicKey candidate);

        void teste();

};

#endif