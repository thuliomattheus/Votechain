#ifndef electorArea_h
#define electorArea_h

#include <iostream>
    using namespace std;

#include "stringUtil.h"

#include "../lib/cryptopp/rsa.h"
    using CryptoPP::RSA;

#include "../lib/cryptopp/osrng.h"
    using CryptoPP::AutoSeededRandomPool;

class ElectorArea{

    private:

    	RSA::PrivateKey privKey;
    	RSA::PublicKey pubKey;

        string getPrivateKeyAsString();
        string getPublicKeyAsString();

    public:

        ElectorArea();

        RSA::PublicKey getPublicKey();

        void testarAssinaturas(RSA::PublicKey pubK);

};

#endif