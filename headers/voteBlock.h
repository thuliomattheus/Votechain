#ifndef voteBlock_h
#define voteBlock_h

#include <iostream>
    using namespace std;

#include <iomanip>
    // put_time

#include <sstream>

#include <chrono>
    using chrono::system_clock;
    using chrono::high_resolution_clock;
    using chrono::duration_cast;

#include "stringUtil.h"

class VoteBlock{

    private:
        string data, hash, previousHash;
        time_t timestamp;
        uint64_t nonce;

    public:
        VoteBlock(string data, string getPreviousHash);

        string getHash();
        string getPreviousHash();
        string getTimestampAsString();

        void setHash();

        string getAttributesAsString();
        void showFullData();
        void mineBlock(int difficulty);
};

#endif