#include "../headers/blockchain.h"

Blockchain::Blockchain(){
    this->deep = 0;
}

Blockchain Blockchain::operator=(Blockchain b){
    return b;
}

void Blockchain::addBlock(Document& data){
    if(this->deep == 0){
        this->createGenesisBlock(data);
    }
    else{
        this->chain.push_back(Block(data, this->chain.back().getHash(), deep));
        this->deep++;
    }
}

void Blockchain::createGenesisBlock(Document& data){
    this->chain.push_back(Block(data, this->genesisPreviousHash, deep));
    this->deep++;
}

void Blockchain::showBlocks(){
    for(vector<Block>::iterator n=this->chain.begin(); n!=this->chain.end(); n++){
        n->showFullData();
    }
}

bool Blockchain::isChainValid(){

    string target(difficulty, '0');
    string aux;

    for(int i=0; i<this->deep; i++){

        Block b1 = this->chain[i];
        aux = StringUtil::applySha256(b1.getAttributesAsString());

        if(i!=0){
            Block b0 = this->chain[i-1];

            if( b1.getHash() != aux ){
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
            if( b1.getHash() !=  aux ){
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

void Blockchain::proofOfWork(int index, int difficulty){

    // Crie uma string de tamanho 'difficulty' composta apenas por zeros
    string target(difficulty, '0');

    auto startTime = high_resolution_clock::now();

    // Enquanto os primeiros 'difficulty' caracteres forem diferentes de 0
    while(this->chain.at(index).getHash().substr(0, difficulty) != target){
        this->chain.at(index).nonce++;
        this->chain.at(index).setHash();
    }
    auto endTime = high_resolution_clock::now();

    cout << "Bloco " << index << " minerado em " << duration_cast<chrono::seconds>(endTime - startTime).count() << " segundos\n\n";

}
