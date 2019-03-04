#ifndef utilities_h
#define utilities_h

#include <iostream>
    using std::cout;
    using std::string;
    using std::endl;

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

#include "../lib/rapidjson/filereadstream.h"
	using rapidjson::FileReadStream;

#include "../lib/rapidjson/document.h"
	using rapidjson::Document;
	using rapidjson::Value;

#include "../lib/rapidjson/stringbuffer.h"
	using rapidjson::StringBuffer;

#include "../lib/rapidjson/writer.h"
	using rapidjson::Writer;


using CryptoPP::SecByteBlock;
using CryptoPP::SHA256;
using CryptoPP::StringSource;
using CryptoPP::HashFilter;
using CryptoPP::StringSink;
using CryptoPP::byte;

namespace Utilities{

    class StringUtil{

        public:

            // Criptografa a dada string utilizando SHA 256
            static string applySha256(string s);

            // Retorna uma chave pública como string
            static string pubKeyAsString(RSA::PublicKey pubK);

            // Retorna uma chave privada como string
            static string privKeyAsString(RSA::PrivateKey privK);

            // Assina uma mensagem utilizando a chave privada do remetente
            static SecByteBlock signMessage(RSA::PrivateKey privK, string message);

            // Verifica a assinatura de uma mensagem com a chave pública do remetente
            static bool verifyMessage(RSA::PublicKey pubK, string message, SecByteBlock signature);

            // Converte um documento para uma string
            static string documentToString(const Document& d);

            // Assina uma mensagem utilizando a chave privada do remetente
            static Document stringToDocument(string s);

            // Assina uma mensagem utilizando a chave privada do remetente
            static Document fileToDoc(string filePath);

    };

}


#endif