#ifndef urn_h
#define urn_h

#include "block.h"

#include "utilities.h"
    using Utilities::StringUtil;

#include <vector>

using namespace std;

class Blockchain{

    private:
        const string genesisPreviousHash = "0000000000000000000000000000000000000000000000000000000000000000";

        void createGenesisBlock(Document& data);

    public:
        Blockchain();
        Blockchain operator=(Blockchain b);

        int deep;
        vector<Block> chain;
        const static int difficulty = 5;

        void addBlock(Document& data);
        void showBlocks();
        bool isChainValid();
        void proofOfWork(int blockIndex, int difficulty);

};

#endif