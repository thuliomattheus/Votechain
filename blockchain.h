#ifndef blockchain_h
#define blockchain_h

#include <iostream>
#include <vector>
#include "block.h"

using namespace std;

class Blockchain{

    private:
        const string genesisPreviousHash = "0000000000000000000000000000000000000000000000000000000000000000";
        int deep;

        void createGenesisBlock(string data);

    public:
        Blockchain(string name);
        vector<Block> chain;
        string name;

        void addBlock(string data);
        void showBlocks();
        bool isChainValid();
        const static int difficulty = 6;

};

#endif