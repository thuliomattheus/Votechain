#ifndef block_h
#define block_h

#include <iostream>
using namespace std;

class Block{

    private:
        string data, hash, previousHash;
        time_t timestamp;

    public:
        Block(string data, string getPreviousHash);

        string getData();
        string getHash();
        string getPreviousHash();
        time_t getTimestamp();
        string getTimestampAsString();

        void setData(string data);
        void setHash();
        void setPreviousHash(string previousHash);

        string getAttributesAsString();
        void printFullDataAsString();
        string calculateHash(string s);

};

#endif