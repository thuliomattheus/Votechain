#Compilador utilizado
CXX = g++
#Todos os avisos (all warnings) e debug
CXXFLAGS = -Wall -g #-H
#Inclusão de bibliotecas
#CXXLIBS = -lcryptopp

#Geração dos objetos com função main passando as libs e os objetos necessários
blockchain: blockchain.o block.o cryptoppLib.o
	$(CXX) $(CXXFLAGS) -o blockchain blockchain.o block.o cryptoppLib.o lib/cryptopp/libcryptopp.a

#cryptoppLib: cryptoppLib.o
#	$(CXX) $(CXXFLAGS) -o teste cryptoppLib.o lib/cryptopp/libcryptopp.a

#Criação dos arquivos compilados das libs abaixo
block.o: block.cpp block.h
	$(CXX) $(CXXFLAGS) -c block.cpp

blockchain.o: blockchain.cpp blockchain.h
	$(CXX) $(CXXFLAGS) -c blockchain.cpp

cryptoppLib.o: cryptoppLib.cpp
	$(CXX) $(CXXFLAGS) -c cryptoppLib.cpp

#Compilação de tudo
all: blockchain;

#Remoção dos arquivos gerados
clean:
	rm -f blockchain keys/* *.o
