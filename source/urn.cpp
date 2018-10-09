#include "../headers/urn.h"

Urn::Urn(string name){
    this->name = name;
    this->deep = 0;

    cout << "Blockchain do " << this->name << "\n\n";
}

void Urn::addBlock(string data){
    if(this->deep == 0){
        this->createGenesisBlock(data);
    }
    else{
        this->chain.push_back(VoteBlock(data, this->chain.back().getHash()));
        this->deep++;
    }
}

void Urn::createGenesisBlock(string data){
    this->chain.push_back(VoteBlock(data, this->genesisPreviousHash));
    this->deep++;
}

void Urn::showBlocks(){
    for(vector<VoteBlock>::iterator n=this->chain.begin(); n!=this->chain.end(); n++){
        n->showFullData();
    }
}

bool Urn::isChainValid(){

    string target(difficulty, '0');
    StringUtil calcHash;
    string aux;

    for(int i=0; i<this->deep; i++){

        VoteBlock b1 = this->chain[i];
        aux = calcHash.applySha256(b1.getAttributesAsString());

        if(i!=0){
            VoteBlock b0 = this->chain[i-1];

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

int main(){

    Urn b("Chelsea");

    b.addBlock("{Jogador : Hazard}");
    b.showBlocks();
    cout << (b.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");
    b.chain.back().mineBlock(b.difficulty);
    b.showBlocks();
    cout << (b.isChainValid() ? "A blockchain é válida\n\n" : "A blockchain é inválida\n\n");

    ElectorArea meuPerfil;

    meuPerfil.testarAssinaturas(meuPerfil.getPublicKey());

    ElectorArea outroPerfil;

    meuPerfil.testarAssinaturas(outroPerfil.getPublicKey());

    // Vote v(meuPerfil.pubKey, meuPerfil.pubKey);

    // v.showHash();

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