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
        this->chain.back().getAttributes();
    }
}

void Blockchain::createGenesisBlock(string data){
    this->chain.push_back(Block(data, "0000000000000000000000000000000000000000000000000000000000000000"));
    this->deep++;
    this->chain.back().getAttributes();
}

int main(){

    Blockchain b("Chelsea");
    b.addBlock("{Jogador : Hazard}");
    sleep(1);
    b.addBlock("{Jogador : Kanté}");
    sleep(1);
    b.addBlock("{Jogador : M. Alonso}");
    sleep(1);
    b.addBlock("{Jogador : Jorginho}");
    sleep(1);
    b.addBlock("{Jogador : Willian}");
    sleep(1);
    b.addBlock("{Jogador : Rudiger}");
    sleep(1);
    b.addBlock("{Jogador : D. Luiz}");
    sleep(1);
    b.addBlock("{Jogador : Barkley}");

    return 0;
}