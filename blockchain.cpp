#include <iostream>
#include <vector>
#include <unistd.h>
#include "blockchain.h"
#include "block.h"

using namespace std;

Blockchain::Blockchain(string name){
    this->name = name;
    this->deep = 0;

    cout << "Blockchain do " << this->name << "\n\n";
}

void Blockchain::addBlock(string data){
    if(this->deep == 0){
        this->createGenesisBlock(data);
    }
    else{
        this->chain.push_back(Block(data, this->chain.back().getHash()));
        this->deep++;
    }
}

void Blockchain::createGenesisBlock(string data){
    this->chain.push_back(Block(data, this->genesisPreviousHash));
    this->deep++;
}

void Blockchain::showBlocks(){
    for(vector<Block>::iterator n=this->chain.begin(); n!=this->chain.end(); n++){
        n->printFullDataAsString();
    }    
}

bool Blockchain::isChainValid(){

    for(int i=0; i<this->deep; i++){

        Block b1 = this->chain[i];

        if(i!=0){
            Block b0 = this->chain[i-1];

            if(b1.getHash() != b1.calculateHash(b1.getAttributesAsString()) ||
                (b1.getPreviousHash() != b0.getHash())){
                return false;
            }
        }
        else{
            if(b1.getHash() != b1.calculateHash(b1.getAttributesAsString()) ||
                b1.getPreviousHash() != this->genesisPreviousHash){
                return false;
            }
        }

    }
    return true;
}

int main(){

/* 
    Block b0("primeiro", "1");
    Block b1("segundo", "2");
    Block b2 = b1;
    b2.getAttributes();
 */
    Blockchain b("Chelsea");

    b.addBlock("{Jogador : Hazard}");
    b.addBlock("{Jogador : Kanté}");
    b.addBlock("{Jogador : M. Alonso}");
    b.addBlock("{Jogador : Jorginho}");
    b.addBlock("{Jogador : Willian}");
    b.addBlock("{Jogador : Rudiger}");
    b.addBlock("{Jogador : D. Luiz}");
    b.addBlock("{Jogador : Barkley}");

    b.showBlocks();
    b.isChainValid();

    return 0;
}