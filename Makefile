#Compilador utilizado
CXX = g++
#Todos os avisos (all warnings) e debug
CXXFLAGS = -Wall -g
#Inclusão de bibliotecas
#CXXLIBS = -lcryptopp

#Geração dos objetos com função main passando as libs e os objetos necessários
blockchain: blockchain.o block.o
	$(CXX) $(CXXFLAGS) -o blockchain blockchain.o block.o lib/cryptopp/libcryptopp.a

#Criação dos arquivos compilados das libs abaixo
block.o: block.cpp block.h
	$(CXX) $(CXXFLAGS) -c block.cpp

blockchain.o: blockchain.cpp blockchain.h
	$(CXX) $(CXXFLAGS) -c blockchain.cpp

#Compilação de tudo
all: blockchain;

#Remoção dos arquivos gerados
clean:
	rm -f block blockchain *.o
