#ifndef block_h
#define block_h

#include <iostream>
    using namespace std;

#include <iomanip>
    //Necessário para usar put_time

#include <sstream>

#include <chrono>
    using chrono::system_clock;
    using chrono::high_resolution_clock;
    using chrono::duration_cast;

#include "utilities.h"
    using Utilities::StringUtil;

class Block{

    private:
        Document& data;
        string hash, previousHash;
        time_t timestamp;
        int index;

    public:
        Block(Document& data, string getPreviousHash, int index);
        uint64_t nonce;

        string getHash();
        string getPreviousHash();
        string getTimestampAsString();

        void setHash();

        string getAttributesAsString();
        void showFullData();
};

#endif