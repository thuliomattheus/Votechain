#include "blockchain.h"

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

    string target(difficulty, '0');

    for(int i=0; i<this->deep; i++){

        Block b1 = this->chain[i];

        if(i!=0){
            Block b0 = this->chain[i-1];

            if( b1.getHash() != b1.calculateHash( b1.getAttributesAsString() ) ){
                return false;
            }
            if( b1.getPreviousHash() != b0.getHash() ){
                return false;
            }
            if( b1.getHash().substr(0, this->difficulty) !=  target){
                return false;
            }
        }
        else{
            if( b1.getHash() != b1.calculateHash( b1.getAttributesAsString() ) ){
                return false;
            }
            if(b1.getPreviousHash() != this->genesisPreviousHash){
                return false;
            }
            if( b1.getHash().substr(0, this->difficulty) !=  target){
                return false;
            }
        }

    }
    return true;
}

int main(){

    Blockchain b("Chelsea");

    b.addBlock("{Jogador : Hazard}");
    b.showBlocks();
    cout << (b.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");
    b.chain.back().mineBlock(b.difficulty);
    b.showBlocks();
    cout << (b.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

    CryptoppLib c;

    string pubK, privK;

    c.generatePairKeyAsString(pubK, privK);

    cout << "A chave pública é : \n" << pubK << "\n\n";
    cout << "A chave privada é : \n" << privK;

    // b.addBlock("{Jogador : Kanté}");
    // b.chain.back().mineBlock(b.difficulty);
    // b.addBlock("{Jogador : M. Alonso}");
    // b.chain.back().mineBlock(b.difficulty);
    // b.addBlock("{Jogador : Jorginho}");
    // b.chain.back().mineBlock(b.difficulty);
    // b.addBlock("{Jogador : Willian}");
    // b.chain.back().mineBlock(b.difficulty);
    // b.addBlock("{Jogador : Rudiger}");
    // b.chain.back().mineBlock(b.difficulty);
    // b.addBlock("{Jogador : D. Luiz}");
    // b.chain.back().mineBlock(b.difficulty);
    // b.addBlock("{Jogador : Barkley}");
    // b.chain.back().mineBlock(b.difficulty);

    // b.showBlocks();
    // cout << b.isChainValid() ? "A blockchain é válida" : "A blockchain é inválida";

    return 0;
}