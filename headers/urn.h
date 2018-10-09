#ifndef urn_h
#define urn_h

#include "voteBlock.h"
#include "vote.h"
#include "electorArea.h"
#include "stringUtil.h"

#include <vector>

using namespace std;

class Urn{

    private:
        const string genesisPreviousHash = "0000000000000000000000000000000000000000000000000000000000000000";
        int deep;

        void createGenesisBlock(string data);

    public:
        Urn(string name);

        vector<VoteBlock> chain;
        string name;
        const static int difficulty = 6;

        void addBlock(string data);
        void showBlocks();
        bool isChainValid();

};

#endif