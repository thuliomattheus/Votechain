#ifndef stringUtil_h
#define stringUtil_h

#include <iostream>
    using std::cout;
    using std::string;

#include "../lib/cryptopp/rsa.h"
    using CryptoPP::RSA;
    using CryptoPP::RSASS;

#include "../lib/cryptopp/base64.h"
    using CryptoPP::Base64Encoder;

#include "../lib/cryptopp/osrng.h"
    using CryptoPP::AutoSeededRandomPool;

#include "../lib/cryptopp/hex.h"
    using CryptoPP::HexEncoder;

#include "../lib/cryptopp/pssr.h"
    using CryptoPP::PSS;

using CryptoPP::SecByteBlock;
using CryptoPP::SHA256;
using CryptoPP::StringSource;
using CryptoPP::HashFilter;
using CryptoPP::StringSink;
using CryptoPP::byte;

class StringUtil{

    public:

        // Criptografa a dada string utilizando SHA 256
        string applySha256(string s);

        // Retorna uma chave pública como string
        string pubKeyAsString(RSA::PublicKey pubK);

        // Retorna uma chave privada como string
        string privKeyAsString(RSA::PrivateKey privK);

        // Assina uma mensagem utilizando a chave privada do remetente
        SecByteBlock signMessage(RSA::PrivateKey privK, string message);

        // Verifica a assinatura de uma mensagem com a chave pública do remetente
        bool verifyMessage(RSA::PublicKey pubK, string message, SecByteBlock signature);

};

#endif