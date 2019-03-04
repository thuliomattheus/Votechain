#ifndef wallet_h
#define wallet_h

#include <iostream>
    using namespace std;

#include "blockchain.h"
#include "transaction.h"

#include "utilities.h"
    using Utilities::StringUtil;

#include "../lib/cryptopp/rsa.h"
    using CryptoPP::RSA;

#include "../lib/cryptopp/osrng.h"
    using CryptoPP::AutoSeededRandomPool;

class Wallet{

    private:

        string name;
        string cpf;
        string voterTitle;
    	RSA::PrivateKey privKey;
    	RSA::PublicKey pubKey;
        Blockchain blockchain;

        // string getPrivateKeyAsString();
        // string getPublicKeyAsString();

    public:

        Wallet(string name, string cpf, string voterTitle);

        string getName();

        RSA::PublicKey getPublicKey();

        Transaction toVote(RSA::PublicKey candidate);

        void updateBlockchain(Blockchain b);

        void teste();

};

#endif