#ifndef block_h
#define block_h

#include <iostream>
    using namespace std;

#include <iomanip>
    // put_time

#include <sstream>

#include <chrono>
    using chrono::system_clock;
    using chrono::high_resolution_clock;
    using chrono::duration_cast;

#include "lib/cryptopp/filters.h"
    using CryptoPP::StringSource;
    using CryptoPP::HashFilter;
    using CryptoPP::StringSink;

#include "lib/cryptopp/hex.h"
    using CryptoPP::HexEncoder;

#include "lib/cryptopp/sha.h"
    using CryptoPP::SHA256;

class Block{

    private:
        string data, hash, previousHash;
        time_t timestamp;
        uint64_t nonce;

    public:
        Block(string data, string getPreviousHash);

        string getData();
        string getHash();
        uint64_t getNonce();
        string getPreviousHash();
        time_t getTimestamp();
        string getTimestampAsString();

        void setData(string data);
        void setHash();
        void setPreviousHash(string previousHash);

        string getAttributesAsString();
        void printFullDataAsString();
        string calculateHash(string s);
        void mineBlock(int difficulty);
};

#endif