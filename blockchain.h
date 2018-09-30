#ifndef blockchain_h
#define blockchain_h

#include <iostream>
#include <vector>
#include "block.h"

using namespace std;

class Blockchain{

    private:
        int deep;
        string name;
        vector<Block> chain;

        void createGenesisBlock(string data);

    public:
        Blockchain(string name);

        void addBlock(string data);

};

#endif