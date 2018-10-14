#ifndef urn_h
#define urn_h

#include "voteBlock.h"
#include "stringUtil.h"

#include <vector>

using namespace std;

class Urn{

    private:
        const string genesisPreviousHash = "0000000000000000000000000000000000000000000000000000000000000000";

        void createGenesisBlock(string data);

    public:
        Urn();

        int deep;
        vector<VoteBlock> chain;
        const static int difficulty = 5;

        void addBlock(string data);
        void showBlocks();
        bool isChainValid();

};

#endif