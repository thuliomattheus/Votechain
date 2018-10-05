#ifndef cryptoppLib_h
#define cryptoppLib_h

#include <iostream>
    using namespace std;

#include "lib/cryptopp/rsa.h"
    using CryptoPP::RSAFunction;
    using CryptoPP::InvertibleRSAFunction;
    using CryptoPP::RSA;

#include "lib/cryptopp/base64.h"
    using CryptoPP::Base64Encoder;

#include "lib/cryptopp/files.h"
    using CryptoPP::FileSink;
    using CryptoPP::FileSource;

#include "lib/cryptopp/osrng.h"
    using CryptoPP::AutoSeededRandomPool;

#include "lib/cryptopp/filters.h"
    using CryptoPP::StringSource;
    using CryptoPP::HashFilter;
    using CryptoPP::StringSink;

#include "lib/cryptopp/hex.h"
    using CryptoPP::HexEncoder;

#include "lib/cryptopp/sha.h"
    using CryptoPP::SHA256;

class CryptoppLib{

    public:
        void generatePairKey();

};

#endif